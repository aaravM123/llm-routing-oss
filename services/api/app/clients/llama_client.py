import time
import random

def call(model_id, prompt, **opts):
    start = time.time()
    time.sleep(0.05)  # simulate ~50ms latency
    latency_ms = int((time.time() - start) * 1000)

    tokens_in = len(prompt.split())  # very rough estimate
    tokens_out = tokens_in + random.randint(5, 10)

    return {
        "text": f"[MOCK] LLaMA response for: {prompt[:40]}...",
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": 0.00,
        "latency_ms": latency_ms
    }

