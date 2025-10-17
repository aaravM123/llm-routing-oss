# agent/llm_clients/common.py
import time

def estimate_tokens(text: str) -> int:
    # ultra-simple: ~1 token ≈ 4 chars (good enough for logging sanity)
    return max(1, int(len(text) / 4))

def simulate_latency(avg_ms: int) -> int:
    start = time.time()
    # don't actually sleep; just compute a near‑avg duration
    # you could time.sleep(avg_ms/1000*0.05) if you want to feel it
    return int((time.time() - start) * 1000) + max(1, int(0.3 * avg_ms))

def compute_cost(tokens_in: int, tokens_out: int, price_in: float, price_out: float) -> float:
    return round((tokens_in/1000.0)*price_in + (tokens_out/1000.0)*price_out, 6)

