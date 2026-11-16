"""
Week 2 Lab - Unit test for LLMClient
GenAI Subject - Y25

Uses a FakeProvider, so this test needs NO API key, NO Ollama and
NO internet. It proves LLMClient works with any provider that has
a generate() method.

Run either way:
    python test_client.py
    python -m pytest test_client.py -v
"""

import unittest

from llm_client import LLMClient


# Fake provider for testing
class FakeProvider:
    def generate(self, prompt):
        return "AI stands for Artificial Intelligence."


class TestLLMClient(unittest.TestCase):
    def test_generate(self):
        provider = FakeProvider()
        client = LLMClient(provider)
        result = client.generate("Explain AI")
        self.assertEqual(
            result,
            "AI stands for Artificial Intelligence.",
        )


if __name__ == "__main__":
    unittest.main()
