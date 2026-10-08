"""
SkillHub Manifest — schema definition and validator for skill manifests.

Every skill folder must contain a ``manifest.json`` file that validates
against SkillManifest.  CI enforces this on every PR.

Required manifest.json schema
------------------------------
{
    "name": "upload_documents",
    "version": "1.0.0",
    "description": "Process and index uploaded documents into MMRAG vector store.",
    "category": "rag",
    "author": "team@company.com",
    "exported_functions": [
        {
            "name": "upload_documents",
            "type": "function",
            "description": "...",
            "inputs": {"upload_folder": "str"},
            "outputs": {"sha_id": "str", "upload_folder": "str", "s3_path": "str"}
        }
    ],
    "env_vars": [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_DEPLOYMENT",
        "AZURE_OPENAI_API_VERSION",
        "AWS_BUCKET_NAME",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_REGION_NAME"
    ],
    "dependencies": "requirements.txt",
    "min_python": "3.10"
}

Usage
-----
    from core.manifest import validate_manifest
    errors = validate_manifest(Path("skills/rag/manifest.json"))
    assert not errors, errors
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional


REQUIRED_FIELDS = {
    "name",
    "version",
    "description",
    "category",
    "author",
    "exported_functions",
    "env_vars",
}


@dataclass
class ExportedFunction:
    name: str
    type: str           # "function" | "agent_factory"
    description: str
    inputs: Dict[str, str] = field(default_factory=dict)
    outputs: Dict[str, str] = field(default_factory=dict)


@dataclass
class SkillManifest:
    name: str
    version: str
    description: str
    category: str
    author: str
    exported_functions: List[ExportedFunction]
    env_vars: List[str]
    dependencies: str = "requirements.txt"
    min_python: str = "3.10"
    changelog: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkillManifest":
        fns = [
            ExportedFunction(**fn) if isinstance(fn, dict) else fn
            for fn in data.get("exported_functions", [])
        ]
        return cls(
            name=data["name"],
            version=data["version"],
            description=data["description"],
            category=data["category"],
            author=data["author"],
            exported_functions=fns,
            env_vars=data.get("env_vars", []),
            dependencies=data.get("dependencies", "requirements.txt"),
            min_python=data.get("min_python", "3.10"),
            changelog=data.get("changelog", []),
        )

    @classmethod
    def load(cls, path: Path) -> "SkillManifest":
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))


def validate_manifest(manifest_path: Path) -> List[str]:
    """
    Validate a manifest.json file.

    Returns a list of error strings.  An empty list means the manifest is valid.

    Used by CI (scripts/validate_manifests.py) and can be called locally.
    """
    errors: List[str] = []

    if not manifest_path.exists():
        return [f"manifest.json not found at {manifest_path}"]

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        return [f"manifest.json is not valid JSON: {exc}"]

    missing = REQUIRED_FIELDS - set(data.keys())
    if missing:
        errors.append(f"Missing required fields: {sorted(missing)}")

    if "version" in data:
        parts = str(data["version"]).split(".")
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            errors.append(f"'version' must be semver (e.g. 1.0.0), got: {data['version']!r}")

    if "exported_functions" in data:
        if not isinstance(data["exported_functions"], list) or len(data["exported_functions"]) == 0:
            errors.append("'exported_functions' must be a non-empty list")
        else:
            for i, fn in enumerate(data["exported_functions"]):
                for req in ("name", "type", "description"):
                    if req not in fn:
                        errors.append(
                            f"exported_functions[{i}] missing required field '{req}'"
                        )

    if "env_vars" in data and not isinstance(data["env_vars"], list):
        errors.append("'env_vars' must be a list of strings")

    return errors
