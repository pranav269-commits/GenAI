# WEEK 2 LAB REPORT
## Provider-Agnostic LLM Client — Gemini (Cloud) + Ollama (Local)

**Subject:** Generative AI (Y25-GenAI) — LAB Experiments
**Experiment:** Week 2 — `week-2`

---

## 1. Aim

To build a provider-agnostic LLM client in Python: a single common
interface (`LLMClient`) that can call either a hosted API (Google
Gemini) or a locally running model (Ollama `llama3.2`), so the calling
program does not change when the provider changes.

## 2. Learning Objectives

After this lab, I can:

1. Define a common interface with an abstract base class (`ABC` / `abstractmethod`).
2. Implement the same `generate(prompt)` method for two very different backends — a cloud API and a local HTTP server.
3. Run a local LLM with Ollama and call it through its REST API at `http://localhost:11434/api/generate`.
4. Keep the Gemini API key in a `.env` file instead of hard-coding it.
5. Unit-test a client using a fake provider, with no key, network, or model needed.

## 3. Software / Requirements

- Windows + PowerShell, Visual Studio Code
- Python with the existing `skill` virtual environment (reused from Week 1)
- Ollama for Windows, model `llama3.2` pulled locally (≈2 GB download)
- Packages (`requirements.txt`): `python-dotenv`, `pytest`, `google-genai`, `requests`
- The Gemini API key from Week 1 (cloud provider only; Ollama needs no key)

## 4. Procedure

1. Installed Ollama on Windows and let it finish starting.
2. In PowerShell, verified the install: `ollama --version`.
3. Downloaded the local model: `ollama pull llama3.2` and confirmed it with `ollama list`.
4. In VS Code, created the folder `week-2` (next to `week-1`) with the files
   `.env`, `llm_client.py`, `main.py`, `test_client.py`, `requirements.txt`.
   *(The file must be `llm_client.py` with an underscore — Python imports
   cannot use the hyphen in the guide's "llm-client.py".)*
5. Activated the existing environment: `..\skill\Scripts\Activate.ps1` — prompt shows `(skill)`.
6. Put the Week 1 Gemini key in `.env` as `GEMINI_API_KEY=...`.
7. Installed packages: `python -m pip install -r requirements.txt`
   *(Guide step 7 reads "pip install requirements.py" — a typo.)*
8. Ran the unit test: `python test_client.py`.
9. Ran the program twice: `python main.py` — once choosing `ollama`,
   once choosing `gemini`, asking the same question both times.

## 5. Programs

### 5.1 `llm_client.py` — the client library

```python
from abc import ABC, abstractmethod

import requests
from google import genai


# Common interface
class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt):
        pass


# Gemini cloud provider
class GeminiProvider(LLMProvider):
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt):
        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        return response.text


# Ollama local provider
class OllamaProvider(LLMProvider):
    def __init__(self, model="llama3.2"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt):
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["response"]


# Common client
class LLMClient:
    def __init__(self, provider):
        self.provider = provider

    def generate(self, prompt):
        return self.provider.generate(prompt)
```

### 5.2 `main.py` — choosing a provider

```python
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
```

### 5.3 `test_client.py` — unit test with a fake provider

```python
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
```

## 6. Code Explanation

| Code element | Purpose |
|---|---|
| `LLMProvider(ABC)` + `@abstractmethod` | Defines the contract: every provider must implement `generate(prompt)`. A provider that doesn't cannot be instantiated. |
| `GeminiProvider.generate()` | Sends the prompt to Google's cloud model `gemini-3.8-flash` via the GenAI SDK and returns `response.text`. Needs the API key + internet. |
| `OllamaProvider.generate()` | POSTs the prompt as JSON to the local Ollama server (`localhost:11434/api/generate`) with `"stream": False`, and returns the `"response"` field. No key, works offline. |
| `LLMClient` | Wraps whichever provider it is given and delegates `generate()` to it — this is what makes the client provider-agnostic. |
| `FakeProvider` (test) | A stand-in with a fixed reply, proving `LLMClient` works with any object that follows the interface. |
| `load_dotenv(override=True)` | Loads `.env` so `os.getenv("GEMINI_API_KEY")` can read the key. |

## 7. Output

**Unit test** (fill in your own run):

```
Ran 1 test in 0.001s

OK
```

**Ollama run** — `[ Paste your terminal screenshot here ]`

```
Choose provider (gemini/ollama): ollama
Enter your question: What is Artificial Intelligence? Explain in simple words.

LLM Response:
<answer generated locally by llama3.2>
```

**Gemini run** — `[ Paste your terminal screenshot here ]`

```
Choose provider (gemini/ollama): gemini
Enter your question: What is Artificial Intelligence? Explain in simple words.

LLM Response:
<answer generated by gemini-3.8-flash>
```

**Observation:** The same `main.py` and the same question produced answers
from two completely different backends. Only the provider object changed.
The Gemini answer arrives in a few seconds from the cloud; the first Ollama
answer is slower (the model loads into memory) but costs nothing, needs no
internet, and the prompt never leaves the laptop.

## 8. Cloud vs Local — comparison

| | Gemini (cloud) | Ollama llama3.2 (local) |
|---|---|---|
| Runs where | Google's servers | Your own laptop |
| API key | Required (`.env`) | Not needed |
| Internet | Required | Only for `ollama pull` |
| Cost / limits | Free-tier rate limits, 503s possible | Free, no rate limit |
| Speed | Fast | Depends on your RAM/GPU; slower first call |
| Privacy | Prompt sent to Google | Prompt stays on your machine |
| Model size/quality | Large hosted model | Small 3B model on disk (≈2 GB) |

## 9. Troubleshooting Reference

| Error | Cause / Fix |
|---|---|
| `ModuleNotFoundError: No module named 'requests'` / `'google'` / `'dotenv'` | Activate the `skill` venv, run `python -m pip install -r requirements.txt` |
| `ConnectionError` on the ollama run | Ollama is not running — start it from the Start menu / system tray and retry |
| `model 'llama3.2' not found` (404) | `ollama pull llama3.2` has not finished — run it and wait |
| Slow first Ollama answer | Normal — the model is loading into memory; later answers are faster |
| `Gemini API key not found in .env` | `.env` in the same folder as `main.py`, spelled exactly `GEMINI_API_KEY` |
| `Invalid provider selected` | Type exactly `gemini` or `ollama` |
| Gemini `503 UNAVAILABLE` | Temporary Google-side overload — wait 2–3 minutes and retry |
| `Activate.ps1 cannot be loaded` | PowerShell execution policy — `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once |

## 10. Result / Conclusion

A single `LLMClient` successfully generated answers from both a hosted
API (Gemini) and a local Ollama model through one common interface, and
the unit test with a fake provider passed. Switching providers required
changing only one line in `main.py` — the provider object passed to
`LLMClient` — demonstrating why applications are built against an
interface instead of a single vendor's API.

## 11. Viva Prep — likely questions

- **Why use an abstract base class?** It forces every provider to implement the same `generate()` method, so the rest of the program can rely on that contract.
- **What makes this client "provider-agnostic"?** `LLMClient` and `main.py` never call Gemini or Ollama directly — they only call `provider.generate()`. A new provider (e.g. OpenAI) only needs a new class with the same method.
- **How does the Ollama call work?** Ollama runs a local server on port 11434. The code POSTs JSON `{model, prompt, stream: false}` to `/api/generate` and reads the `response` field. `"stream": False` means one complete reply instead of token-by-token chunks.
- **Cloud vs local trade-off?** Cloud = bigger models, fast, but needs internet, a key, and has rate limits. Local = private, offline, free, but limited by your hardware and model size.
- **Why can the test run without a key or Ollama?** It injects a `FakeProvider` — dependency substitution. The test verifies `LLMClient`'s behaviour, not any real model.
- **What is `response.raise_for_status()` for?** It turns an HTTP error (e.g. 404 model not found) into an exception immediately, instead of failing later on a missing `response` key.
- **Why is the key in `.env`, not in code?** Code is shared/committed; a leaked key can be misused. `.env` stays local and is git-ignored.
