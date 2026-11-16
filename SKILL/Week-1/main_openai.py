"""
Week 1 Lab - First LLM API Call Using OpenAI (reference version)
Kept for reference only. You are running the Gemini version (main.py),
so you do NOT need this file or an OpenAI key.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found. Check that .env exists "
        "and contains OPENAI_API_KEY=your_key."
    )

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-5.5",
    input="What is Artificial Intelligence? Explain in simple words.",
)

print("\nLLM Response:")
print(response.output_text)
