"""
Week 2 Lab - Run the provider-agnostic LLM client
GenAI Subject - Y25

Run:  python main.py
Then type  gemini  or  ollama  when asked, and enter your question.
The rest of the program is identical for both providers - that is
the whole point of the common LLMClient interface.
"""

import os

from dotenv import load_dotenv

from llm_client import GeminiProvider, LLMClient, OllamaProvider

load_dotenv(override=True)

provider_name = input("Choose provider (gemini/ollama): ").strip().lower()

if provider_name == "gemini":
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Gemini API key not found in .env")
    provider = GeminiProvider(api_key)
elif provider_name == "ollama":
    provider = OllamaProvider("llama3.2")
else:
    raise ValueError("Invalid provider selected")

client = LLMClient(provider)

prompt = input("Enter your question: ")
answer = client.generate(prompt)

print("\nLLM Response:")
print(answer)
