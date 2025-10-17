import time
import random


def call(model_id, prompt, **opts):
    start = time.time()
    time.sleep(random.uniform(0.25, 0.7))

    tokens_in = len(prompt.split())
    tokens_out = random.randint(60, 140)

    price_in = opts.get("price_in", 0.0005)
    price_out = opts.get("price_out", 0.0005)

    cost_usd = (tokens_in / 1000 * price_in) + (tokens_out / 1000 * price_out)

    return {
        "text": f"[Gemini:{model_id}] Echo: {prompt}",
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": round(cost_usd, 6),
        "latency_ms": round((time.time() - start) * 1000, 2),
        "raw": {"status": "simulated"},
    }
