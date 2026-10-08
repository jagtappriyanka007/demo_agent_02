# <Skill Name> Skill — <Tagline>

**Category:** `<category>` | **Version:** `1.0.0` | **Tier:** 1 (FunctionTool)

## What It Does

*Replace this with a clear description of what problem this skill solves and what it returns.*

---

## Exported Functions

### `<function_name>(<param1>, <param2>) → dict`

| Parameter | Type | Description |
|---|---|---|
| `<param1>` | `str` | ... |
| `<param2>` | `int` | ... |

**Returns:** `{"<key1>": ..., "<key2>": ...}`

---

## Quick Start

### 1. Required environment variables (`.env`)

```env
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_DEPLOYMENT=...
AZURE_OPENAI_API_VERSION=...
# Add any skill-specific vars here
```

### 2. Wire in `agents_definition.py`

```python
from skills.<skill_folder_name>.skill import <function_name>
from agents import Agent

def build_agents(model):
    my_agent = Agent(
        name="My Agent",
        instructions="...",
        model=model,
        tools=[<function_name>],
    )
    return my_agent
```

### 3. Install dependencies

```bash
pip install -r skills/<skill_folder_name>/requirements.txt
```

---

## Internal Folder Structure

```
skills/<skill_folder_name>/
├── skill.py              ← import from here only
├── manifest.json
├── requirements.txt
├── tests/
│   └── test_<skill_name>_skill.py
└── _tools/              ← internal — never import directly from your project
    ├── __init__.py
    └── ...
```
