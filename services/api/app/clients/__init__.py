# agent/llm_clients/__init__.py
from . import openai_client, anthropic_client, gemini_client, llama_client, mistral_client

REGISTRY = {
    "openai": openai_client,
    "anthropic": anthropic_client,
    "google": gemini_client,
    "meta": llama_client,
    "mistral": mistral_client,
}

def call(provider: str, model_cfg: dict, prompt: str, **opts):
    client = REGISTRY[provider]
    return client.call(model_cfg, prompt, **opts)

