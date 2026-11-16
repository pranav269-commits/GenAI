# Week 4 — Tokenizer Lab

Compares three pretrained subword tokenizers on the **same** sentences
in English, Telugu and Hindi:

| Tokenizer | Idea | Model |
|---|---|---|
| BPE | Merge frequent adjacent symbol pairs (byte-level) | `gpt2` |
| WordPiece | Learned subword vocab; unknown words split into pieces | `bert-base-multilingual-cased` |
| SentencePiece | Learns subwords directly from raw text | `xlm-roberta-base` |

Fair-comparison note (from the lab): these are real pretrained
tokenizers, not three algorithms trained on the same data. GPT-2 is
mostly English-trained, BERT/XLM-R are multilingual — so count
differences reflect both the method *and* each model's training.
Expect GPT-2 to use many more tokens for Telugu/Hindi.

## Files
- `tokenizer_comparison.py` — the complete lab program
- `requirements.txt` — transformers, sentencepiece
- `output.txt` — a verified sample run (your token IDs should match;
  they only change if Hugging Face updates a tokenizer file)

## Run in VS Code (PowerShell terminal)
Extract `week-4` into `C:\Users\PRANAV\Desktop\KLH\Generative AI\`,
open that folder in VS Code, then:

```powershell
..\skill\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python tokenizer_comparison.py
```

**First run needs internet** — it downloads the three pretrained
tokenizer files from Hugging Face (small files, but XLM-R and mBERT
are the bigger two). After that it works offline from the local cache.

## What to look at in the output
- English: all three give similar, low counts.
- Telugu / Hindi: GPT-2 (BPE) explodes into byte pieces, while
  WordPiece and SentencePiece stay compact — that contrast is the
  main observation for your record/viva (Questions 6 and 7 in the lab).
