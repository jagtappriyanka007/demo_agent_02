# New Agent Project — Starter Template

This folder is a copy-paste starter for new agent projects that consume skills
from `skills/` in this repo (e.g. `my_skill`).

---

## 5-Minute Setup

### Step 1 — Copy this template into your project

```bash
mkdir ../my-agent-project
cp -r templates/new_agent_project/* ../my-agent-project/
cp -r core/ ../my-agent-project/core/
cp -r skills/my_skill ../my-agent-project/skills/my_skill
```

Your project structure should look like:
```
my-agent-project/
├── core/                          ← from this repo
├── skills/
│   └── my_skill/   ← from this repo
├── agents_definition.py           ← from this template — edit this
├── api.py                         ← from this template — minor edits
├── .env                           ← copy from .env.example and fill in
└── requirements.txt                ← combine skill requirements.txt files
```

### Step 2 — Configure `.env`

```bash
cp .env.example .env
# Edit .env with your Azure OpenAI (and any skill-specific) credentials
```

### Step 3 — Edit `agents_definition.py`

Uncomment the block for `my_skill` (or any other skills
you copied in). Wire prompts and agent names.

### Step 4 — Install dependencies

```bash
python -m venv .venv && source .venv/bin/activate
cat skills/my_skill/requirements.txt >> requirements.txt
pip install -r requirements.txt
pip install fastapi uvicorn
```

### Step 5 — Run

```bash
uvicorn api:app --host 0.0.0.0 --port 8080 --reload
```

Test:
```bash
curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

---

## Files in This Template

| File | Purpose |
|---|---|
| `agents_definition.py` | Wire skills into agents — **edit this** |
| `api.py` | FastAPI server with `/invoke`, `/invoke-stream`, `/health` |
| `.env.example` | Environment variable template — copy to `.env` |

---

## When to Add a New Skill

If the skill you need doesn't exist yet in `skills/`:
1. Use `templates/new_skill/` as a starting point
2. Write your skill in `skills/<new_skill_name>/`
3. Test it (`pytest skills/<new_skill_name>/tests/ -v`), then wire it here
