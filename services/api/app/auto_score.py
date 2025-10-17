import os
import random
from typing import List, Dict

# Step 3: Auto-scoring logic (API optional)
def score_responses(prompt: str, responses: List[Dict]) -> List[Dict]:
    """
    Scores model outputs.
    If API key is available, use GPT-based scoring.
    If not, use a fallback mock scoring method.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    updated = []

    if api_key:
        # Real scoring using OpenAI API
        try:
            import openai
            openai.api_key = api_key
            import json

            for r in responses:
                scoring_prompt = f"""
You are an expert evaluator. Score the following AI model output for the prompt "{prompt}".
Criteria: relevance, clarity, factual correctness, and completeness.
Return ONLY a JSON object: {{ "score": number from 0 to 5, "reason": short explanation }}.

Output to score:
---
{r['response']}
---
"""
                try:
                    completion = openai.ChatCompletion.create(
                        model="gpt-4o-mini",  # cheap + fast for scoring
                        messages=[
                            {"role": "system", "content": "You are a strict and concise evaluator."},
                            {"role": "user", "content": scoring_prompt}
                        ],
                        temperature=0
                    )

                    score_data = json.loads(completion.choices[0].message["content"])
                    r["score"] = score_data.get("score", 0)
                    r["reason"] = score_data.get("reason", "")
                except Exception as e:
                    r["score"] = -1
                    r["reason"] = f"Scoring failed: {str(e)}"

                updated.append(r)
        except ImportError:
            # Fallback if openai package not installed
            for r in responses:
                r["score"] = random.randint(1, 5)  # Random mock score
                r["reason"] = "(Mock) OpenAI package not installed"
                updated.append(r)

    else:
        # Step 4: Fallback mock scoring when no API key is provided
        for r in responses:
            r["score"] = random.randint(1, 5)  # Random mock score
            r["reason"] = "(Mock) Random score assigned since API key not set"
            updated.append(r)

    # Sort by score (highest first)
    updated.sort(key=lambda x: x["score"], reverse=True)
    return updated

# Example usage
if __name__ == "__main__":
    test_prompt = "Explain quantum computing in one sentence."
    test_responses = [
        {"model": "OpenAI GPT-4o", "response": "Quantum computing uses quantum bits to perform complex computations much faster than classical computers.", "latency": 389.77, "tokens_in": 6, "tokens_out": 57, "cost": 0.0001},
        {"model": "Claude 3 Opus", "response": "Quantum computing harnesses quantum mechanics to process information in ways classical computers cannot.", "latency": 489.92, "tokens_in": 6, "tokens_out": 99, "cost": 0.0003},
        {"model": "Gemini 1.5 Pro", "response": "Quantum computing uses qubits and quantum entanglement to process data differently than traditional computers.", "latency": 418.31, "tokens_in": 6, "tokens_out": 123, "cost": 0.0001}
    ]

    ranked = score_responses(test_prompt, test_responses)
    print("\nLeaderboard:")
    for r in ranked:
        print(f"{r['model']} - Score: {r['score']} - {r['reason']}")

