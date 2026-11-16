# Week 3 — MongoDB Connectivity: LLM Monitoring

Week 2's provider-agnostic LLM client, upgraded: every call (Gemini or
Ollama) is timed, token-counted, costed, and **logged into MongoDB**
(database `llm_monitoring`, collection `call_logs`).

## Files
- `main.py` — menu: 1 = Gemini, 2 = Ollama; asks a question, prints the answer
- `llm_client.py` — LLMProvider / GeminiProvider / OllamaProvider / LLMClient
  (3-attempt retry on temporary errors only, latency + cost on every call)
- `mongo_logger.py` — MongoLogger: inserts one document per call into MongoDB
- `cost_calculator.py` — sample per-1M-token pricing; Ollama always costs 0.0
- `requirements.txt` — pytest, google-genai, python-dotenv, pymongo, requests
- `.env` — put your Gemini key here (copy it from your week-1 `.env`)
- `test_week3.py` — offline test with a fake provider/logger (no MongoDB needed)

## Before you run (one-time, from the Week 3 document)
1. Finish installing the MongoDB MSI that is downloading, then in
   **PowerShell**:
   `Get-Service MongoDB`  → if it is not Running: `Start-Service MongoDB`
   (run PowerShell as Administrator if Start-Service says access denied)
2. Open **MongoDB Compass**, connect to `mongodb://localhost:27017`,
   create database **llm_monitoring** with collection **call_logs**.
   (MongoLogger also creates them automatically on the first logged call,
   but the lab asks you to create them in Compass.)
3. Ollama: `llama3.2` is already pulled from Week 2 — nothing to redo.
   Just make sure the Ollama app is running if you pick provider 2.

## Run in VS Code (PowerShell terminal)
Extract `week-3` into `C:\Users\PRANAV\Desktop\KLH\Generative AI\`,
open that folder in VS Code, then:

```powershell
..\skill\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python test_week3.py
python main.py
```

After a run, refresh `llm_monitoring > call_logs` in Compass — one new
document per call with provider, model, prompt, tokens, latency_ms,
cost, attempts and status.

## Guide fixes applied (kept from Weeks 1-2 pattern)
1. Document's Gemini model was `gemini-3-flash-pro`, but its own PRICING
   table only lists `gemini-3.8-flash` — cost would always be None.
   Model aligned to `gemini-3.8-flash` (verified working in Weeks 1-2).
2. `requests` was missing from the document's requirements.txt even
   though llm_client.py imports it — added.
3. mongo_logger.py defined `close()` twice in the document — kept once.
