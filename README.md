# My Skill

One sentence describing what this skill does.

Generated from the SkillHub skill cookiecutter template — follows the folder
structure and `@skill` conventions defined in
[skillhub-base-template](https://github.com/HARMAN-DTS/skillhub-base-template).

## Structure

```
demo_agent_02/
├── core/                        <- skill infrastructure (never edit)
│   ├── decorators.py             @skill, @agent_skill
│   ├── registry.py               list_skills(), get_skill(), print_catalog()
│   └── manifest.py               manifest.json schema validator
├── skills/
│   └── my_skill/
│       ├── .env.example          copy -> .env, fill in credentials
│       ├── skill.py              public API - @skill decorated functions only
│       ├── manifest.json         skill metadata + contract
│       ├── requirements.txt      pip dependencies
│       ├── tests/
│       │   └── test_skill.py     three mandatory tests
│       └── _tools/
│           └── src/              paste your agent / pipeline code here
├── templates/
│   ├── new_skill/                copy-paste starter for the next skill you add
│   └── new_agent_project/        copy-paste starter for a new agent project
├── setup.py                      Cython build script
├── pyproject.toml                build config
└── .gitignore
```

**Key rules:**
- `core/` is frozen — never edit it
- Everything you write goes inside `skills/my_skill/`
- `skill.py` is the only public surface — agents import only from here
- `_tools/` is private — no one outside the skill imports from it directly
- `manifest.json` is the contract — validated by `core/manifest.py`

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

pip install -r skills/my_skill/requirements.txt openai-agents python-dotenv pytest

copy skills\my_skill\.env.example skills\my_skill\.env
# cp skills/my_skill/.env.example skills/my_skill/.env   (macOS/Linux)
# then fill in your credentials

pytest skills/my_skill/tests/ -v
```

Expected output:
```
PASSED tests/test_skill.py::test_skill_importable
PASSED tests/test_skill.py::test_skill_registered
PASSED tests/test_skill.py::test_manifest_valid
```

## Implementing Your Skill

1. Open `skills/my_skill/skill.py` and replace the example
   `my_skill_run` body with your real logic (currently just
   echoes the input in upper case).
2. Put any private implementation code under `_tools/` (and `_tools/src/` for
   larger packages, e.g. a LangGraph pipeline).
3. Update `manifest.json` — `description`, `inputs`, `outputs`, `env_vars`.
4. Add/adjust tests in `tests/test_skill.py`. All three mandatory tests must
   keep passing.

## Adding Another Skill

Copy `templates/new_skill/` to `skills/<new_skill_name>/` and follow the
`# CHANGE` / `<PLACEHOLDER>` comments inside.

## Packaging (Cython)

```bash
python setup.py build_ext --inplace
python setup.py bdist_wheel
```

See `setup.py` for the folder scan configuration.
