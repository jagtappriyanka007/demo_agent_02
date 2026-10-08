"""
Skill decorators — the only two primitives every skill author needs.

Three tiers of skills
=====================

Tier 1 & 2 — Function skills  (@skill)
---------------------------------------
Any plain Python function (stateless or stateful via closures).
The decorator wraps it with ``function_tool`` → FunctionTool, which can be
passed directly into ``Agent(tools=[...])``.  

Bridge mode (auto-detected) — state-dict functions
----------------------------------------------------
When ``@skill`` is applied to a function whose sole parameter is annotated
with a TypedDict subclass (LangGraph nodes, AutoGen steps, etc.), the
decorator activates **bridge mode** automatically:

  - It reads the TypedDict's own ``__annotations__`` to build a fully
    typed wrapper (``_bridge``) that the OpenAI function_tool can introspect.
  - The ``_bridge`` is registered in ``_SKILL_REGISTRY`` as the FunctionTool.
  - The **original function is returned unchanged** so the framework
    (LangGraph, AutoGen, ADK, …) sees zero change.

Decorator stacking rule — place ``@skill`` BELOW any framework decorator
(closer to the function) so it always receives the raw function:

    @staticmethod                # applied second — sees original fn back
    @skill(name="x", ...)        # applied first  — sees raw fn, returns it unchanged
    def my_node(state: MyState) -> dict:
        ...


Tier 3 — Agent factory  (@agent_skill)
---------------------------------------
ONLY for sub-systems built entirely with the OpenAI Agents SDK where
``Agent(handoffs=[...])`` is the intended wiring.  For any non-SDK system
(LangGraph, REST, custom Python) use ``@skill`` and return the result as a
plain dict — handoffs cannot reach outside the SDK Runner loop.

    from core.decorators import agent_skill

    @agent_skill(name="my_pipeline", description="...", category="pipeline")
    def build_my_pipeline(model) -> Agent:
        sub = Agent(name="Sub", ...)
        return Agent(name="Entry", ..., handoffs=[sub])

    # In agents_definition.py:
    from skills.markdown_editing.skill import build_markdown_pipeline
    entry_agent = build_markdown_pipeline(model)
    Agent(handoffs=[entry_agent])


Registry
--------
Every decorated skill is automatically added to ``_SKILL_REGISTRY``:
    {
        "type": "function" | "agent",
        "fn": <wrapped FunctionTool or raw factory>,
        "original_fn": <unwrapped callable>,   # function skills only
        "description": str,
        "category": str,
    }
"""

import inspect
from inspect import Parameter, Signature
from typing import Callable, Dict, Any

from agents import function_tool

_SKILL_REGISTRY: Dict[str, Dict[str, Any]] = {}


def _is_typed_dict(annotation) -> bool:
    """
    Return True if *annotation* is a TypedDict subclass.

    TypedDicts are regular dict subclasses that also carry
    ``__annotations__``, ``__required_keys__``, and ``__optional_keys__``.
    Checking all three avoids false-positives from plain dicts or other
    dict subclasses.
    """
    try:
        return (
            isinstance(annotation, type)
            and issubclass(annotation, dict)
            and hasattr(annotation, "__annotations__")
            and hasattr(annotation, "__required_keys__")
            and hasattr(annotation, "__optional_keys__")
        )
    except TypeError:
        return False


def skill(name: str, description: str, category: str, depends_on: list = None):
    """
    Universal skill decorator — two modes, one decorator.

    Parameters
    ----------
    name : str
        Unique skill identifier (snake_case).  Used as the function_tool
        name visible to the LLM.
    description : str
        One-sentence description of what the skill does.  Shown to the LLM.
    category : str
        Logical grouping: "rag", "markdown", "domain", "bre", "pipeline", …
    depends_on : list[str], optional
        Advisory list of other skill names whose output feeds this skill.
        Stored in the registry for documentation; does not affect runtime.

    Returns
    -------
    Normal mode  — FunctionTool replacing the function.
    Bridge mode  — original function unchanged; FunctionTool in registry only.

    Mode selection (automatic)
    --------------------------
    Bridge mode activates when the decorated function has **exactly one
    parameter** annotated with a TypedDict subclass (e.g. a LangGraph node).
    In bridge mode the decorator:
      1. Reads the TypedDict's ``__annotations__`` to build a typed ``_bridge``
         wrapper with a proper ``inspect.Signature``.
      2. Wraps ``_bridge`` with ``function_tool`` and stores it in the registry.
      3. Returns the **original function unchanged** — the framework is unaware
         that ``@skill`` ran at all.

    Normal mode activates for all other signatures (existing behaviour,
    100% backward-compatible).
    """

    def decorator(fn: Callable) -> Any:
        sig    = inspect.signature(fn)
        params = list(sig.parameters.values())

        # ── Bridge mode: single TypedDict-annotated parameter ─────────────
        if (
            len(params) == 1
            and params[0].annotation is not Parameter.empty
            and _is_typed_dict(params[0].annotation)
        ):
            state_class = params[0].annotation
            fields      = state_class.__annotations__   # {field_name: type}

            def _bridge(**kwargs):
                # Build state dict from provided kwargs; strip None values
                # so nodes that check ``state.get(key)`` behave naturally.
                state  = {k: v for k, v in kwargs.items() if v is not None}
                result = fn(state)
                return result if isinstance(result, dict) else {}

            _bridge.__signature__ = Signature([
                Parameter(
                    field,
                    Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=typ,
                    default=None,   # all optional — TypedDict is total=False
                )
                for field, typ in fields.items()
            ])
            _bridge.__name__ = name
            _bridge.__doc__  = description

            wrapped = function_tool(_bridge)
            _SKILL_REGISTRY[name] = {
                "type":        "function",
                "fn":          wrapped,
                "original_fn": _bridge,
                "description": description,
                "category":    category,
                "depends_on":  depends_on or [],
            }

            return fn   # ← original returned UNCHANGED; framework unaffected

        # ── Normal mode: existing behaviour, 100% unchanged ───────────────
        fn.__doc__ = description
        fn._skill_meta = {"name": name, "description": description, "category": category}

        wrapped = function_tool(fn)

        _SKILL_REGISTRY[name] = {
            "type":        "function",
            "fn":          wrapped,
            "original_fn": fn,
            "description": description,
            "category":    category,
            "depends_on":  depends_on or [],
        }

        return wrapped

    return decorator


def agent_skill(name: str, description: str, category: str):
    """
    Tier 3 decorator — register an Agent factory for SDK-native sub-agent
    pipelines that use ``Agent(handoffs=[...])``.

    The factory is returned **unchanged** (not wrapped).  Callers invoke it
    as a constructor:  ``entry = build_pipeline(model)`` then wire with
    ``Agent(handoffs=[entry])``.

    IMPORTANT — use ``@skill`` (not ``@agent_skill``) when the sub-system is
    a LangGraph graph, a REST API, or any non-SDK orchestrator.  Those must
    be plain FunctionTools.

    Parameters
    ----------
    name : str
        Unique factory identifier.
    description : str
        What the pipeline does.
    category : str
        Logical grouping (typically "pipeline").
    """

    def decorator(fn: Callable) -> Callable:
        fn.__doc__ = fn.__doc__ or description
        fn._skill_meta = {"name": name, "description": description, "category": category}

        _SKILL_REGISTRY[name] = {
            "type": "agent",
            "fn": fn,
            "description": description,
            "category": category,
        }

        return fn  # no wrapping — factory stays a plain callable

    return decorator
