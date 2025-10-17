from fastapi import FastAPI
import sentry_sdk
import os
from dotenv import load_dotenv

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv(
        "SENTRY_DSN",
        "https://fc9682d97f2f117fac6dfe11fb43fa2c@o4510203843837952.ingest.us.sentry.io/4510203851505664",
    ),
    send_default_pii=True,
    traces_sample_rate=1.0,
)

app = FastAPI(title="LLM Router OSS")


@app.get("/")
async def root():
    return {"message": "LLM Router OSS API", "status": "running"}


@app.post("/query")
async def query(payload: dict):
    prompt = payload.get("prompt")
    mode = payload.get("mode", "balanced")
    # basic example pipeline - router engine to be implemented
    # from router_engine import select_model
    # model_info = select_model(prompt, mode)
    return {
        "selected_model": {"provider": "openai", "model_id": "gpt-4o-mini"},
        "prompt": prompt,
        "mode": mode,
        "note": "Router engine implementation pending",
    }
