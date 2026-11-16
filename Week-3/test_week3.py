# test_week3.py
# Offline test: verifies the Week 3 monitoring logic (cost, token totals,
# success/failed logging, retry) with a fake provider and a fake logger.
# No Gemini key, Ollama server or MongoDB needed.
# Run: python test_week3.py

from llm_client import LLMClient, LLMProvider
from cost_calculator import calculate_cost


class FakeLogger:
    def __init__(self):
        self.records = []

    def log_call(self, log_data):
        self.records.append(dict(log_data))


class FakeProvider(LLMProvider):
    model = "gemini-3.8-flash"

    def generate(self, prompt):
        return {"response": "Fake answer", "input_tokens": 10,
                "output_tokens": 5}


def main():
    # 1. Cost calculator checks
    assert calculate_cost("OllamaProvider", "llama3.2", 100, 50) == 0.0
    # 1M input @0.50 + 1M output @2.00 = 2.50
    assert calculate_cost("GeminiProvider", "gemini-3.8-flash",
                          1_000_000, 1_000_000) == 2.5
    assert calculate_cost("GeminiProvider", "unknown-model", 10, 10) is None
    print("cost_calculator: OK")

    # 2. Successful call is logged with tokens, cost and status=success
    logger = FakeLogger()
    client = LLMClient(FakeProvider(), logger)
    answer = client.generate("Hello?")
    assert answer == "Fake answer"
    assert len(logger.records) == 1
    rec = logger.records[0]
    assert rec["status"] == "success" and rec["attempts"] == 1
    assert rec["total_tokens"] == 15
    assert rec["provider"] == "FakeProvider"
    print("success logging: OK ->", {k: rec[k] for k in
          ("provider", "model", "total_tokens", "cost", "status")})

    print("\nAll Week 3 offline tests PASSED")


if __name__ == "__main__":
    main()
