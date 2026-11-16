# Week 3 (Atlas version) — LLM Monitoring with MongoDB Atlas

Same Week 3 problem as the local version, but MongoDB runs **in the
cloud (MongoDB Atlas, free M0 cluster)** instead of a local Community
Server install. **No 925 MB download, no Compass install needed** —
records are viewed in the Atlas website (Browse Collections).

> You now have TWO Week 3 variants. Use the one your teacher assigned:
> - `week-3` (local) — Community Server + Compass, db `llm_monitoring`,
>   collection `call_logs`, logger file `mongo_logger.py`, menu `1/2`
> - `week-3-atlas` (this one) — Atlas cloud, db `llm_monitoring`,
>   collection `api_usage`, logger file `usage_logger.py`, menu
>   type `gemini` / `ollama`, cost rates read from `.env`

## Files (exactly as this document specifies)
- `main.py` — choose provider by typing `gemini` or `ollama`
- `llm_client.py` — providers return an `LLMResult` dataclass; the client
  measures latency, estimates cost from `.env` rates, retries temporary
  errors (up to 3 attempts, 1s then 2s)
- `usage_logger.py` — UsageLogger: connects via `MONGODB_URI`, pings the
  cluster, inserts one document per call into `api_usage`, retries a
  failed write 3 times
- `test_client.py` — the document's own unittest (fake provider/logger)
- `requirements.txt` — python-dotenv, google-genai, requests, pymongo, pytest
- `.env` — template; YOU fill in the three values below on your laptop

## One-time Atlas setup (document Part 2 — only you can do this,
## it needs your own sign-in; do NOT paste the URI/password in chat)
1. mongodb.com → Atlas → sign up/sign in with Google
2. Create a cluster → **Free (M0)** → nearby region → name it
   e.g. `GenAICluster` → Create Deployment, wait until ready
3. Create a **database user** (e.g. `genai_user`) with a strong
   password — this is a database password, not your website login;
   save it in your password manager
4. Network Access → Add IP Address → **Add My Current IP Address**
   (the document specifically says avoid 0.0.0.0/0)
5. Cluster → Connect → Drivers → Python → copy the connection string.
   It looks like `mongodb+srv://genai_user:<password>@...` — replace
   `<password>` with your database user's password

## Fill .env (inside the week-3-atlas folder on your laptop)
```
GEMINI_API_KEY=<copy from your week-1 .env>
MONGODB_URI=<the Atlas string from step 5>
GEMINI_INPUT_PRICE_PER_MILLION=0.50
GEMINI_OUTPUT_PRICE_PER_MILLION=2.00
```
The two price lines are the sample rates (not verified current Gemini
prices) so estimated cost is not always 0. Never upload `.env` to GitHub.

## Run in VS Code (PowerShell terminal)
Extract into `C:\Users\PRANAV\Desktop\KLH\Generative AI\`, open the
`week-3-atlas` folder, then:

```powershell
..\skill\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest test_client.py
python main.py
```

Type `gemini` or `ollama` when asked. Afterwards, in Atlas:
your cluster → Browse Collections → `llm_monitoring` → `api_usage`
shows one document per call (provider, model, tokens, latency_ms,
estimated_cost_usd, status, attempts, timestamp).
