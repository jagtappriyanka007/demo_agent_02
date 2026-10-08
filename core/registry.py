"""
SkillHub Registry — query the catalog of registered skills.

Skills are auto-registered via @skill / @agent_skill decorators when their
module is imported.  This module provides read-only query helpers.

Usage
-----
    from core.registry import list_skills, get_skill, get_skills_by_category

    for name, meta in list_skills().items():
        print(f"{name} [{meta['category']}] — {meta['description']}")
"""

from typing import Dict, Any, Optional

from core.decorators import _SKILL_REGISTRY


def list_skills() -> Dict[str, Dict[str, Any]]:
    """Return a snapshot of all registered skills keyed by name."""
    return dict(_SKILL_REGISTRY)


def get_skill(name: str) -> Optional[Dict[str, Any]]:
    """
    Return metadata for a single skill by name, or None if not found.

    Example
    -------
        meta = get_skill("upload_documents")
        tool = meta["fn"]   # FunctionTool or factory
    """
    return _SKILL_REGISTRY.get(name)


def get_skills_by_category(category: str) -> Dict[str, Dict[str, Any]]:
    """Return all skills whose category matches the given string."""
    return {
        name: meta
        for name, meta in _SKILL_REGISTRY.items()
        if meta.get("category") == category
    }


def print_catalog() -> None:
    """Print a human-readable catalog of all registered skills to stdout."""
    if not _SKILL_REGISTRY:
        print("No skills registered.  Import skill modules first.")
        return

    from itertools import groupby

    grouped = {}
    for name, meta in sorted(_SKILL_REGISTRY.items(), key=lambda x: x[1]["category"]):
        grouped.setdefault(meta["category"], []).append((name, meta))

    print("\n=== SkillHub Catalog ===\n")
    for category, items in sorted(grouped.items()):
        print(f"[{category.upper()}]")
        for name, meta in items:
            tier = "Tier 3 (agent factory)" if meta["type"] == "agent" else "Tier 1/2 (function tool)"
            print(f"  {name:<35} {tier}")
            print(f"    {meta['description']}")
        print()
