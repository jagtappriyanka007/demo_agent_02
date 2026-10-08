"""
My Skill Skill — One sentence describing what this skill does.

Exports
-------
my_skill_run : @skill — One sentence describing what this skill does.

Internal dependencies (_tools/)
--------------------------------
None yet — put your implementation code under _tools/ (and _tools/src/ for
larger packages / LangGraph pipelines) and import it lazily from here.

Usage (in your agents_definition.py)
--------------------------------------
    from skills.my_skill.skill import my_skill_run
    from agents import Agent

    my_agent = Agent(
        name="My Agent",
        instructions="...",
        model=model,
        tools=[my_skill_run],
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
    name="my_skill_run",
    description=(
        "One sentence describing what this skill does."
    ),
    category="domain",
)
def my_skill_run(input_text: str) -> dict:
    """
    Example implementation — replace with your real logic.

    Parameters
    ----------
    input_text : str
        Input text to process.

    Returns
    -------
    dict
        {"result": str} — the processed output.
    """
    # ── Implementation ────────────────────────────────────────────────────────
    # Import your tool classes here (from _tools/) to keep them lazy-loaded.
    # from _tools.my_tool import MyTool
    # return MyTool.run(input_text)

    return {"result": input_text.upper()}


# ── Tier 3 template (agent factory) — delete if not needed ──────────────────
# @agent_skill(
#     name="build_my_skill_pipeline",
#     description="<What the multi-agent sub-system does.>",
#     category="pipeline",
# )
# def build_my_skill_pipeline(model) -> Agent:
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
