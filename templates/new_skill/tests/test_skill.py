"""Tests for <skill_name> skill.

These must pass in CI. Add at minimum:
  1. test_skill_importable — the skill module imports without error
  2. test_skill_registered — the skill appears in the registry
  3. test_manifest_valid  — manifest.json passes schema validation

For live/integration tests, guard with:
  @pytest.mark.skipif(not os.getenv("SKILLHUB_LIVE_TEST"), reason="Set SKILLHUB_LIVE_TEST=1")
"""

import os
import pytest
from pathlib import Path


def test_skill_importable():
    from skills.<skill_folder_name>.skill import <function_name>
    assert <function_name> is not None


def test_skill_registered():
    import skills.<skill_folder_name>.skill  # noqa: F401
    from core.registry import get_skill

    meta = get_skill("<function_name>")
    assert meta is not None, "<function_name> not found in registry"
    assert meta["category"] == "<category>"
    assert meta["type"] == "function"


def test_manifest_valid():
    from core.manifest import validate_manifest
    errors = validate_manifest(Path(__file__).parent.parent / "manifest.json")
    assert errors == [], f"Manifest validation errors: {errors}"


@pytest.mark.skipif(
    not os.getenv("SKILLHUB_LIVE_TEST"),
    reason="Set SKILLHUB_LIVE_TEST=1 to run live integration tests",
)
def test_live_<function_name>():
    """Live test — requires real credentials in environment."""
    from skills.<skill_folder_name>.skill import <function_name>
    result = <function_name>(<param1>="test_value", <param2>=1)
    assert isinstance(result, dict)
    # Add assertions on expected output keys
