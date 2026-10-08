"""Tests for my_skill skill.

These must pass in CI. Includes the three mandatory tests:
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
    from skills.my_skill.skill import my_skill_run
    assert my_skill_run is not None


def test_skill_registered():
    import skills.my_skill.skill  # noqa: F401
    from core.registry import get_skill

    meta = get_skill("my_skill_run")
    assert meta is not None, "my_skill_run not found in registry"
    assert meta["category"] == "domain"
    assert meta["type"] == "function"


def test_manifest_valid():
    from core.manifest import validate_manifest
    errors = validate_manifest(Path(__file__).parent.parent / "manifest.json")
    assert errors == [], f"Manifest validation errors: {errors}"


@pytest.mark.skipif(
    not os.getenv("SKILLHUB_LIVE_TEST"),
    reason="Set SKILLHUB_LIVE_TEST=1 to run live integration tests",
)
def test_live_my_skill_run():
    """Live test — requires real credentials/environment if applicable."""
    from skills.my_skill.skill import my_skill_run
    result = my_skill_run(input_text="hello")
    assert isinstance(result, dict)
    assert result["result"] == "HELLO"
