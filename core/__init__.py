"""
SkillHub Core — skill infrastructure.

Import from here to register and discover skills:
    from core.decorators import skill, agent_skill
    from core.registry import list_skills, get_skill
"""

from core.decorators import skill, agent_skill, _SKILL_REGISTRY
from core.registry import list_skills, get_skill, get_skills_by_category

__all__ = [
    "skill",
    "agent_skill",
    "_SKILL_REGISTRY",
    "list_skills",
    "get_skill",
    "get_skills_by_category",
]
