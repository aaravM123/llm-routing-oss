from fastapi import FastAPI

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
