# Week 1 Lab — First LLM API Call (Gemini version)

**Subject:** GenAI (Y25) | **Your provider:** Gemini — `main.py` is already set up for it

## Files

| File | What it is |
|---|---|
| `main.py` | The program you run — Gemini version, model `gemini-3.8-flash` |
| `main_openai.py` | OpenAI version, reference only — you don't need it |
| `.env` | Where YOUR Gemini key goes — currently blank, see Step 2 |
| `.env.example` | Template showing the exact format |
| `.gitignore` | Stops `.env`, `.venv/` and caches being committed to Git |
| `requirements.txt` | `google-genai`, `python-dotenv` |
| `LAB_REPORT.md` | Completed lab write-up for your record |

## Run it (VS Code, Windows)

Folder: `C:\KLH\2026-2027\Subjects\Y25-GenAI\LAB_Experiments\week1-llm-call`

1. Copy these files into that folder. Open it in VS Code, Terminal → New Terminal.
2. **Add your key:** open `.env`, paste your Gemini key after the `=` — no quotes, no spaces:
   `GEMINI_API_KEY=AIza...your key...`
   Never screenshot or share this file. Don't paste the key in any chat.
3. **Activate the existing venv** — if the prompt doesn't show `(.venv)`:
   `..\.venv\Scripts\Activate.ps1`
4. **Install packages (once):** `python -m pip install -r requirements.txt`
5. **Run:** `python main.py`

**Expected:** `LLM Response:` followed by a simple-words explanation of AI.
Wording changes every run — that's normal.

## Then do the lab's prompt experiments

Change only the `contents=` text in `main.py`, re-run each time, screenshot each output:

1. `Explain Generative AI with two real-world examples.`
2. `What is a Large Language Model? Explain for a first-year engineering student.`
3. `Differentiate Artificial Intelligence, Machine Learning, and Deep Learning.`

## Quick fixes

| Error | Fix |
|---|---|
| `No module named 'google'` / `'dotenv'` | venv not active, or re-run Step 4 |
| `Gemini API key not found!` | `.env` next to `main.py`, named exactly `.env` (not `.env.txt`), variable exactly `GEMINI_API_KEY` |
| `400 / 403 API key not valid` | Key copied wrong or revoked — re-copy it from Google AI Studio |
| `429 quota / rate limit` | Free-tier limit hit — wait a minute and retry |
| `503 UNAVAILABLE / high demand` | Google's model is temporarily overloaded — not your fault. `main.py` now retries and falls back to `gemini-3.6-flash` / `gemini-2.5-flash` automatically |
| `Model not found` | Replace `gemini-3.8-flash` in `main.py` with `gemini-2.5-flash` |
