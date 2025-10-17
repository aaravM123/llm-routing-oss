import time
import random


def call(model_id, prompt, **opts):
    start = time.time()

    # Simulate processing delay
    time.sleep(random.uniform(0.2, 0.6))

    # Fake token counts
    tokens_in = len(prompt.split())  # crude estimate
    tokens_out = random.randint(50, 150)

    # Simulate cost (example OpenAI rates from config)
    price_in = opts.get("price_in", 0.0015)  # per 1K tokens
    price_out = opts.get("price_out", 0.002)

    cost_usd = (tokens_in / 1000 * price_in) + (tokens_out / 1000 * price_out)

    return {
        "text": f"[OpenAI:{model_id}] Echo: {prompt}",
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": round(cost_usd, 6),
        "latency_ms": round((time.time() - start) * 1000, 2),
        "raw": {"status": "simulated"},
    }
