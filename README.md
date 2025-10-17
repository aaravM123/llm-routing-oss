# LLM Router OSS

A lightweight **backend routing system** for intelligent LLM selection across multiple providers.

Supports:
- **OpenAI** - GPT-4o, GPT-4o-mini
- **Anthropic** - Claude 3 Sonnet
- **Google Gemini** - Gemini 1.5 Pro
- **Meta** - LLaMA 3 70B
- **Mistral** - Mistral Large

---

## Features

- Smart model routing based on prompt complexity and mode (fast/balanced/accurate)
- Redis and local caching to reduce redundant API calls
- Token usage and cost tracking
- Structured logging for all LLM requests
- Auto-scoring system for response quality evaluation
- FastAPI backend with clean REST API

---

## Architecture

### Core Components

1. **Router Engine** (`router_engine.py`) - Intelligent model selection logic
2. **Caching Layer** (`caching.py`) - Redis/local cache with TTL support
3. **Logging Utils** (`logging_utils.py`) - Per-call and daily rollup tracking
4. **LLM Clients** (`clients/`) - Unified interface for all providers
5. **Auto Scorer** (`auto_score.py`) - Automated response quality evaluation

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/llm-router-oss.git
cd llm-router-oss
pip install -r requirements.txt
```

### API Keys

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=...
GEMINI_API_KEY=...
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_SECONDS=86400
```

If keys are missing, models will run in mock/simulation mode.

---

## Usage

### Start the FastAPI server

```bash
cd services/api/app
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Endpoints

**POST /query**

Request body:
```json
{
  "prompt": "Explain quantum computing in one sentence",
  "mode": "balanced"
}
```

Response:
```json
{
  "selected_model": {
    "provider": "openai",
    "model_id": "gpt-4o-mini",
    "estimated_cost": 0.0001
  },
  "prompt": "Explain quantum computing in one sentence"
}
```

---

## Project Structure

```
llm-router-oss/
├── LICENSE
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
└── services/
    └── api/
        └── app/
            ├── main.py              # FastAPI entry point
            ├── router_engine.py     # Model selection logic
            ├── caching.py           # Cache layer
            ├── logging_utils.py     # Logging utilities
            ├── auto_score.py        # Response scoring
            ├── config.yaml          # Model catalog & settings
            └── clients/             # LLM provider clients
                ├── __init__.py
                ├── common.py
                ├── openai_client.py
                ├── anthropic_client.py
                ├── gemini_client.py
                ├── mistral_client.py
                └── llama_client.py
```

---

## Configuration

All settings are in `services/api/app/config.yaml`:

- Model catalog with pricing and latency estimates
- Cache backend (local or Redis)
- Logging paths
- Default routing mode

Example:

```yaml
mode: balanced

models:
  openai_gpt4o_mini:
    provider: openai
    id: gpt-4o-mini
    price_in: 0.0005
    price_out: 0.0015
    avg_latency_ms: 800

cache:
  backend: local
  ttl_seconds: 86400
  redis_url: "redis://localhost:6379/0"

logging:
  per_call_path: "./logs/per_call.jsonl"
  daily_rollup_path: "./logs/daily.json"
```

---

## Caching

The system supports two cache backends:

1. **Local** - Uses pickle files for persistence
2. **Redis** - For distributed/production environments

Cache keys include:
- Model ID
- Prompt hash
- Mode (fast/balanced/accurate)
- Tools signature
- Version tag

---

## Logging

Two logging levels:

1. **Per-call logs** (`logs/per_call.jsonl`) - Every request with full metadata
2. **Daily rollups** (`logs/daily.json`) - Aggregated stats by day and model

Tracked metrics:
- Tokens in/out
- Cost in USD
- Latency in ms
- Cache hit/miss
- Auto-score ratings

---

## Mock Mode

If API keys are not configured, clients automatically run in mock mode:
- Simulated latency
- Fake token counts
- Zero cost
- Responses marked `[MOCK]`

Perfect for testing and development without spending on API calls.

---

## Contributing

Contributions welcome! Please submit issues and pull requests.

---

## License

This project is open source under the [Apache-2.0 License](LICENSE).

