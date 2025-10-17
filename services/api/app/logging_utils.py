"""
Logging utilities for tracking API calls and generating daily rollups.
"""

import json
import os
import time
import uuid
import hashlib
import datetime
from typing import Dict, Any


def ensure_dirs(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def now_iso() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"


def start_timer() -> float:
    return time.time()


def end_timer(start: float) -> int:
    return int((time.time() - start) * 1000)  # ms


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def log_call(per_call_path: str, data: Dict[str, Any]) -> None:
    ensure_dirs(per_call_path)
    with open(per_call_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def _load_daily(daily_path: str) -> Dict[str, Any]:
    if not os.path.exists(daily_path):
        return {}
    try:
        with open(daily_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_daily(daily_path: str, payload: Dict[str, Any]) -> None:
    ensure_dirs(daily_path)
    with open(daily_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def update_daily_rollup(daily_path: str, call: Dict[str, Any]) -> None:
    daily = _load_daily(daily_path)
    day = call["timestamp"][:10]  # YYYY-MM-DD
    model = call.get("model", "unknown")

    if day not in daily:
        daily[day] = {
            "totals": {
                "calls": 0,
                "tokens_in": 0,
                "tokens_out": 0,
                "cost_usd": 0.0,
                "latency_ms_sum": 0,
                "cache_hits": 0,
            },
            "by_model": {},
        }

    if model not in daily[day]["by_model"]:
        daily[day]["by_model"][model] = {
            "calls": 0,
            "tokens_in": 0,
            "tokens_out": 0,
            "cost_usd": 0.0,
            "latency_ms_sum": 0,
            "cache_hits": 0,
        }

    # Update helpers
    def add(acc, call):
        acc["calls"] += 1
        acc["tokens_in"] += int(call.get("tokens_in", 0))
        acc["tokens_out"] += int(call.get("tokens_out", 0))
        acc["cost_usd"] += float(call.get("cost_usd", 0.0))
        acc["latency_ms_sum"] += int(call.get("latency_ms", 0))
        if call.get("cache_hit"):
            acc["cache_hits"] += 1

    add(daily[day]["totals"], call)
    add(daily[day]["by_model"][model], call)
    _save_daily(daily_path, daily)


def build_call_record(
    per_call_cfg: dict,
    prompt: str,
    model: str,
    mode: str,
    tokens_in: int = 0,
    tokens_out: int = 0,
    cost_usd: float = 0.0,
    latency_ms: int = 0,
    cache_hit: bool = False,
    auto_score: float | None = None,
    human_score: float | None = None,
    request_id: str | None = None,
) -> dict:
    return {
        "timestamp": now_iso(),
        "request_id": request_id or str(uuid.uuid4()),
        "prompt_hash": sha256_text(prompt),
        "model": model,
        "mode": mode,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": round(cost_usd, 6),
        "latency_ms": latency_ms,
        "cache_hit": cache_hit,
        "eval": {
            "auto_score": auto_score,
            "human_score": human_score,
        },
        **per_call_cfg,  # optional: extra fields if you want
    }
