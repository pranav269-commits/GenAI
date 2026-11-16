# GenAI — Generative AI Lab (Y25)

Lab work for the Generative AI subject at KLH: weekly Python labs that build
from a first LLM API call up to a provider-agnostic client with MongoDB
usage monitoring, plus a tokenizer comparison lab.

## Contents

| Folder | Lab | What it does |
| --- | --- | --- |
| `Week-1` | First LLM API call | Calls the Gemini API from Python (`gemini-3.8-flash`, with retry and model fallback). `main_openai.py` is the OpenAI reference version. |
| `Week-2` | Provider-agnostic LLM client | One `LLMClient` interface over Gemini (cloud) and Ollama `llama3.2` (local), with a FakeProvider test. |
| `Week-3` | MongoDB connectivity — LLM monitoring | Week 2 client + logging of tokens, latency and cost for every call into local MongoDB (`llm_monitoring` database, `call_logs` collection, via Compass/Community Server). |
| `Week-3-Atlas` | LLM monitoring with MongoDB Atlas | Same monitoring lab using a cloud Atlas cluster instead (`api_usage` collection, `MONGODB_URI` in `.env`). |
| `Week-4` | Tokenizer lab | Compares GPT-2 (BPE), mBERT (WordPiece) and XLM-R (SentencePiece) token counts on English, Telugu and Hindi text. |

## Setup

Each week is self-contained:

```powershell
cd Week-1            # or any week folder
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` in the week folder and add your own
`GEMINI_API_KEY` (and `MONGODB_URI` for Week-3-Atlas). **Never commit a
real `.env` file** — it is covered by `.gitignore`.

Run commands and expected output are documented in each week's own
`README.md`.
