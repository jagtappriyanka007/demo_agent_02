# My Skill Skill — One sentence describing what this skill does.

**Category:** `domain` | **Version:** `1.0.0` | **Tier:** 1 (FunctionTool)

## What It Does

One sentence describing what this skill does.

*Replace this section with a clear description of what problem this skill solves and what it returns.*

---

## Exported Functions

### `my_skill_run(input_text) → dict`

| Parameter | Type | Description |
|---|---|---|
| `input_text` | `str` | Text to process |

**Returns:** `{"result": ...}`

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
from skills.my_skill.skill import my_skill_run
from agents import Agent

def build_agents(model):
    my_agent = Agent(
        name="My Agent",
        instructions="...",
        model=model,
        tools=[my_skill_run],
    )
    return my_agent
```

### 3. Install dependencies

```bash
pip install -r skills/my_skill/requirements.txt
```

### 4. Run the tests

```bash
pytest skills/my_skill/tests/ -v
```

---

## Internal Folder Structure

```
skills/my_skill/
├── skill.py              ← import from here only
├── manifest.json
├── requirements.txt
├── tests/
│   └── test_skill.py
└── _tools/              ← internal — never import directly from your project
    ├── __init__.py
    └── src/
```
