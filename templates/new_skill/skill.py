"""
<SKILL_NAME> Skill — <one-line description>

Replace every <PLACEHOLDER> with your actual values.

Exports
-------
<function_name> : @skill — <what it does>

Internal dependencies (_tools/)
--------------------------------
List any files in _tools/ that this skill uses.

Usage (in your agents_definition.py)
--------------------------------------
    from skills.<skill_folder>.skill import <function_name>
    from agents import Agent

    my_agent = Agent(
        name="My Agent",
        instructions="...",
        model=model,
        tools=[<function_name>],
    )
"""

import sys
import os

# Add _tools to path so internal imports work
_tools_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_tools")
if _tools_dir not in sys.path:
    sys.path.insert(0, _tools_dir)

from core.decorators import skill

# ── Uncomment and adapt if you need a Tier 3 agent factory ──────────────────
# from core.decorators import agent_skill
# from agents import Agent, ModelSettings


@skill(
    name="<function_name>",           # snake_case, unique across SkillHub
    description=(
        "<One sentence describing exactly what this skill does. "
        "This description is shown to the LLM — be precise about inputs and outputs.>"
    ),
    category="<category>",            # e.g. "rag", "domain", "markdown", "bre", "pipeline"
)
def <function_name>(<param1>: str, <param2>: int) -> dict:
    """
    <Docstring — describe the function for human readers, not for the LLM.
    The LLM uses the description= argument above.>

    Parameters
    ----------
    <param1> : str
        <What it is and what values are expected.>
    <param2> : int
        <What it is.>

    Returns
    -------
    dict
        {"<key1>": <type>, "<key2>": <type>}
        Describe what each key means.
    """
    # ── Implementation ────────────────────────────────────────────────────────
    # Import your tool classes here (from _tools/) to keep them lazy-loaded.
    # from _tools.my_tool import MyTool
    # return MyTool.run(<param1>, <param2>)

    raise NotImplementedError("Replace this with your implementation.")


# ── Tier 3 template (agent factory) — delete if not needed ──────────────────
# @agent_skill(
#     name="build_<name>_pipeline",
#     description="<What the multi-agent sub-system does.>",
#     category="pipeline",
# )
# def build_<name>_pipeline(model) -> Agent:
#     """Factory: build and wire a multi-agent sub-system."""
#     sub_agent = Agent(name="SubAgent", instructions="...", model=model, tools=[])
#     entry = Agent(name="OrchestratorAgent", model=model, handoffs=[sub_agent])
#     return entry


# ── Bridge mode (LangGraph / AutoGen / ADK — optional) ───────────────────────
# Use this section ONLY if your skill wraps a framework node whose calling
# convention is a single state TypedDict argument.  @skill auto-detects the
# TypedDict and activates bridge mode — no extra parameters needed.
#
# Stacking rule: @skill MUST be closer to the function than @staticmethod
# (or any other framework decorator).  Python applies decorators bottom-up,
# so @skill fires first and returns the original function unchanged.
#
# from core.registry import get_skill
#
# def _register_component_skills():
#     """Import node module — fires @skill bridge registrations as side effect."""
#     _tools_src = os.path.join(os.path.dirname(__file__), "_tools", "src")
#     if _tools_src not in sys.path:
#         sys.path.insert(0, _tools_src)
#     from <your_package>.pipeline.graph import MyGraphProcessor  # noqa: F401
#
# _register_component_skills()
#
# # Pull the FunctionTools out of the registry and give them importable names
# <node_skill_name> = get_skill("<node_skill_name>")["fn"]
