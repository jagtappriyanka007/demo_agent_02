"""
API entry point for <Your Project Name>.

This is a minimal FastAPI + OpenAI Agents SDK server.
Adapt the /invoke endpoint to match your project's input model.

Streams are supported — use /invoke-stream for a streaming variant.
"""

import os
import json
import warnings

from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional

from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from agents import Runner, OpenAIChatCompletionsModel, set_default_openai_client, set_tracing_disabled

from agents_definition import build_agents

load_dotenv()
warnings.filterwarnings("ignore")

# ── Azure OpenAI client ───────────────────────────────────────────────────────
azure_openai_client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
)
set_default_openai_client(azure_openai_client)
set_tracing_disabled(True)

model = OpenAIChatCompletionsModel(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    openai_client=azure_openai_client,
)

# ── Agent initialization ──────────────────────────────────────────────────────
# build_agents() is the only place agents are constructed.
supervisor = build_agents(model)

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(title="My Skill")


class QueryInput(BaseModel):
    message: str
    # Add any additional input fields your project needs:
    # document_path: Optional[str] = None
    # user_id: Optional[str] = "default"


@app.post("/invoke")
async def invoke(query_input: QueryInput):
    """
    Synchronous invoke — runs the agent pipeline and returns the final output.
    Suitable for short requests (< ~30s).
    """
    runner = Runner()
    result = await runner.run(supervisor, query_input.message)
    return JSONResponse(content={"response": result.final_output})


@app.post("/invoke-stream")
async def invoke_stream(query_input: QueryInput):
    """
    Streaming invoke — yields agent events as newline-delimited JSON.
    Use for long-running requests or real-time UIs.
    """
    async def event_generator():
        async with Runner().run_streamed(supervisor, query_input.message) as stream:
            async for event in stream.stream_events():
                yield json.dumps({"event": type(event).__name__}) + "\n"
        yield json.dumps({"done": True, "output": stream.final_output}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=True)
