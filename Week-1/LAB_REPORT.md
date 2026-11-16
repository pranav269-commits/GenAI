# WEEK 1 LAB REPORT
## First LLM API Call Using Gemini

*(The lab guide gives OpenAI as the primary route and Gemini as the alternative.
This experiment was completed with a **Gemini API key**, using the guide's
Gemini code in `main.py`. The OpenAI version is kept as `main_openai.py`.)*

**Subject:** Generative AI (Y25-GenAI) — LAB Experiments
**Experiment:** Week 1 — `week1-llm-call`

---

## 1. Aim

To connect a Python program to a Large Language Model (LLM) using an API,
send a prompt to the model, and display the generated response — with the
API key stored securely in a `.env` file instead of hard-coded in the code.

## 2. Learning Objectives

After this lab, I can:

1. Explain the role of an API key when connecting a Python application to an LLM.
2. Install and use an LLM Python SDK (Google GenAI SDK here; OpenAI SDK in the guide) in an existing virtual environment.
3. Store an API key securely in a `.env` file instead of hard-coding it.
4. Send a prompt to the model and display the generated response.
5. Recognize and troubleshoot common setup, authentication, quota, and model errors.

## 3. Software / Requirements

- Visual Studio Code
- Python (project virtual environment `.venv`, reused — no second venv created)
- Packages (`requirements.txt`): `google-genai`, `python-dotenv`
- A Gemini API key created in Google AI Studio
- Internet connectivity

> **Note:** For the OpenAI route in the guide, ChatGPT access and OpenAI API
> access are separate — a ChatGPT subscription does not automatically provide
> API credits. The Gemini route used here works on the Gemini API free tier
> for this model, subject to rate limits.

## 4. Procedure

1. Opened the existing project folder `week1-llm-call` in VS Code
   (File → Open Folder) and opened a new terminal.
2. Confirmed the virtual environment was active — terminal prompt shows `(.venv)`.
   If not, activated it with `..\.venv\Scripts\Activate.ps1`.
3. Created `.env` in the project folder and stored the key in it:
   `GEMINI_API_KEY=<my key>` — no quotes, never shared or committed.
4. Created `.gitignore` containing `.env`, `.venv/`, `__pycache__/`, `.pytest_cache/`
   so the secret file and caches are never committed to Git.
5. Created `main.py` (code in Section 5).
6. Installed dependencies: `python -m pip install -r requirements.txt`
7. Ran the program: `python main.py`
8. Observed the output, then repeated with different prompts (Section 7).

## 5. Program — `main.py`

```python
import os

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

# Step 4: Make first LLM call
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="What is Artificial Intelligence? Explain in simple words.",
)

# Step 5: Display response
print("\nLLM Response:")
print(response.text)
```

*Robustness added in the submitted `main.py`: the call above is wrapped in a
retry + fallback loop. A `503 UNAVAILABLE` response means the model is
temporarily overloaded on Google's side (observed during this lab's first
live run with `gemini-3.8-flash`) — it is not a code, key, or quota error.
The program waits 10 seconds and retries each model twice, then falls back
to `gemini-3.6-flash`, then `gemini-2.5-flash`, and prints which model
actually answered.*

*OpenAI alternative (`main_openai.py`): same flow — `load_dotenv()`, read
`OPENAI_API_KEY`, `OpenAI(api_key=api_key)`, then
`client.responses.create(model="gpt-5.5", input="...")`
and print `response.output_text`.*

## 6. Code Explanation

| Code element | Purpose |
|---|---|
| `import os` | Provides access to environment variables. |
| `from dotenv import load_dotenv` | Imports the function that loads values from the `.env` file. |
| `from google import genai` | Imports the Google GenAI SDK client. |
| `load_dotenv()` | Loads variables defined in the local `.env` file into the process environment. |
| `os.getenv("GEMINI_API_KEY")` | Reads the API key without writing the secret directly in the Python source. |
| `genai.Client(api_key=api_key)` | Creates an authenticated Gemini API client. |
| `client.models.generate_content(...)` | Sends the prompt (`contents`) to the selected model (`gemini-3.8-flash`). |
| `response.text` | Gets the generated text from the response. |

## 7. Output

**Expected / sample format** (exact wording varies — the model generates it fresh each run):

```
LLM Response:
Artificial Intelligence is a way of making computers smart. It teaches a
computer to learn from examples, understand language, recognize things,
and make decisions — similar to how a human brain learns from experience,
but using data and mathematics instead of thoughts.
```

**[ Paste your own terminal screenshot here after your run — crop out the `.env` file. ]**

### Prompt experiments (lab Section 9)

Only the `contents=` text was changed, model kept the same, program re-run each time:

1. `Explain Generative AI with two real-world examples.`
2. `What is a Large Language Model? Explain for a first-year engineering student.`
3. `Differentiate Artificial Intelligence, Machine Learning, and Deep Learning.`

**Observation:** More specific prompts give more focused, level-appropriate
answers. Adding the audience ("for a first-year engineering student") and the
format ("with two real-world examples", "Differentiate...") changes the
structure and depth of the response, even though the model is unchanged.

## 8. Troubleshooting Reference

| Error | Cause / Fix |
|---|---|
| `ModuleNotFoundError: No module named 'google'` | Activate `.venv`, run `python -m pip install google-genai` |
| `ModuleNotFoundError: No module named 'dotenv'` | Run `python -m pip install python-dotenv` |
| `Gemini API key not found!` | `.env` in same folder as `main.py`, spelled exactly `GEMINI_API_KEY`, file not named `.env.txt` |
| `400 / 403 API key not valid` | Key copied incorrectly or revoked. Re-copy it from Google AI Studio. Never paste the key in a chat to debug |
| `429 quota / rate-limit` | Free-tier rate limit or quota hit — wait and retry, check usage in AI Studio |
| `503 UNAVAILABLE — model experiencing high demand` | Temporary overload on Google's side, not your code or key. Wait and re-run, or use a fallback model — handled automatically by the retry/fallback loop in `main.py` |
| `Model not found / model access error` | Replace the model ID with one available to your project, e.g. `gemini-2.5-flash` |
| Connection / timeout | Check internet, VPN/proxy, retry after a short interval |

## 9. Result / Conclusion

The Python program successfully connects to the LLM through the API using a
securely stored key, sends a prompt, and displays the model's generated
response. Changing only the prompt text changes the response, demonstrating
how an LLM API can be integrated into any Python application.

## 10. Viva Prep — likely questions

- **What is an API key?** A secret credential that identifies and authenticates
  your application/project to the API provider; usage and billing are tracked against it.
- **Why store it in `.env` and not in code?** Code gets shared/committed; a leaked
  key can be misused and billed to you. `.env` stays local and is blocked by `.gitignore`.
  If a key is ever published, revoke it and generate a new one.
- **What does `load_dotenv()` do?** Reads the `.env` file and loads its variables
  into the process environment so `os.getenv()` can read them.
- **ChatGPT subscription vs API access?** Separate products and billing. ChatGPT
  does not give API credits.
- **Why does the output differ each run?** LLMs generate text probabilistically;
  the same prompt can produce differently worded answers.
- **What is `requirements.txt` for?** Records the project's packages so anyone can
  recreate the environment with `python -m pip install -r requirements.txt`.
- **What is a virtual environment?** An isolated Python environment for one project,
  so its package versions do not conflict with other projects.
