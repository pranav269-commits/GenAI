# Week 2 Lab — Provider-Agnostic LLM Client (Gemini + Ollama)

**Subject:** GenAI (Y25) | **Idea:** one `LLMClient`, two interchangeable providers

## Files

| File | What it is |
|---|---|
| `llm_client.py` | The library: `LLMProvider` interface, `GeminiProvider`, `OllamaProvider`, `LLMClient` — note the **underscore**, not `llm-client.py` |
| `main.py` | The program you run — asks `gemini` or `ollama`, then your question |
| `test_client.py` | Unit test with a `FakeProvider` — no key, no Ollama, no internet needed |
| `requirements.txt` | `python-dotenv`, `pytest`, `google-genai`, `requests` |
| `.env` | Where YOUR Week 1 Gemini key goes — currently blank |
| `.env.example` | Template showing the exact format |
| `LAB_REPORT.md` | Completed lab write-up for your record |

## Run it (VS Code, Windows PowerShell)

Your folder: `C:\Users\PRANAV\Desktop\KLH\Generative AI\week-2`
Your venv: `skill` (in the `Generative AI` root, same one as Week 1)

1. Copy these files into the `week-2` folder. Open that folder in VS Code, Terminal → New Terminal.
2. **Activate the venv** — if the prompt doesn't show `(skill)`:
   `..\skill\Scripts\Activate.ps1`
3. **Add your key (for the Gemini run only):** open `.env`, paste the same Gemini key from Week 1 after the `=` — no quotes, no spaces. Never screenshot this file, never paste the key in a chat.
4. **Install packages (once):** `python -m pip install -r requirements.txt`
   *(The guide's step 7 says `pip install requirements.py` — that's a typo in the guide.)*
5. **Check Ollama first (new PowerShell window):**
   `ollama --version` then `ollama pull llama3.2` then `ollama list`
   Leave Ollama running (system tray icon) — the local provider talks to it at `http://localhost:11434`.
6. **Run the test:** `python test_client.py` — expected: `OK` (1 test)
7. **Run Ollama:** `python main.py` → type `ollama` → ask a question. First answer can take 20–60 seconds while the model loads.
8. **Run Gemini:** `python main.py` → type `gemini` → ask the same question. Screenshot both outputs for your report.

## Quick fixes

| Error | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'requests'` / `'google'` / `'dotenv'` | venv not active (no `(skill)` in prompt), or re-run Step 4 |
| `ConnectionError` / `Failed to establish a connection` on ollama | Ollama isn't running — launch it from the Start menu, wait a few seconds, re-run |
| `model 'llama3.2' not found` | Run `ollama pull llama3.2` and wait for the download to finish |
| `Gemini API key not found in .env` | `.env` next to `main.py`, variable spelled exactly `GEMINI_API_KEY`, no `.env.txt` |
| `Invalid provider selected` | Type exactly `gemini` or `ollama` at the first prompt |
| Gemini `503 UNAVAILABLE / high demand` | Google-side overload, not your code — wait 2–3 minutes and re-run; the Ollama run still works offline meanwhile |
| PowerShell blocks `Activate.ps1` | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then activate again |
