"""
Week 1 Lab - First LLM API Call Using Gemini
GenAI Subject - Y25

What this program does:
1. Loads the API key securely from a .env file (never hard-coded).
2. Creates a Gemini client.
3. Sends a prompt to the model and prints the generated response.

Updated: if a model replies 503 UNAVAILABLE ("high demand" - a temporary
Google-side overload, not a code or key error), the program waits a few
seconds and retries, then automatically tries the next model in the list.
"""

import os
import time

from dotenv import load_dotenv
from google import genai

# Step 1: Load API key from .env
load_dotenv()

# Step 2: Read Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "Gemini API key not found! Check that .env exists in this folder "
        "and contains GEMINI_API_KEY=your_key."
    )

# Step 3: Initialize Gemini client
client = genai.Client(api_key=api_key)

PROMPT = "What is Artificial Intelligence? Explain in simple words."

# Step 4: Make the first LLM call - with retry + fallback for 503 errors
# First choice is the lab's model; the others are only used if it is busy.
MODELS = ["gemini-3.8-flash", "gemini-3.6-flash", "gemini-2.5-flash"]

response = None
last_error = None

for model in MODELS:
    for attempt in range(1, 3):  # try each model up to 2 times
        try:
            response = client.models.generate_content(
                model=model,
                contents=PROMPT,
            )
            print(f"(Model used: {model})")
            break
        except Exception as error:
            last_error = error
            if "503" in str(error) or "UNAVAILABLE" in str(error):
                print(f"{model} is busy (503, high demand). Retrying...")
                time.sleep(10)
            else:
                # Not a busy error (e.g. bad key) - do not retry, stop here.
                raise
    if response is not None:
        break
    print(f"{model} is still busy. Trying the next model...")

if response is None:
    raise RuntimeError(
        "All models are busy right now (503). This is temporary - "
        "wait 2-3 minutes and run the program again."
    ) from last_error

# Step 5: Display response
print("\nLLM Response:")
print(response.text)
