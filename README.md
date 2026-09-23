# EduGenie — Google Gemini Powered Learning Assistant

A lightweight AI-powered educational assistant. Ask questions, get
concept explanations, generate quizzes, summarize passages, and get
personalized learning paths.

## 1. Requirements

- Python 3.10+
- A free Google Gemini API key: https://aistudio.google.com/app/apikey

## 2. Setup

```bash
# from inside the EduGenie folder
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

```

> `torch` + `transformers` (used for the local explanation model) are
> a few GB combined and take a few minutes to install. If you'd rather
> skip the local model for now, see "Optional: skip the local model"
> below.

## 3. Add your Gemini API key

```bash
cp .env.example .env
```

Open `.env` and paste your real key:

```
GEMINI_API_KEY=your_actual_key_here
```

## 4. Run it

```bash
uvicorn main:app --reload
```

Open **http://127.0.0.1:8000** in your browser.

The first time you use "Explain a concept," it will download the
LaMini-Flan-T5-783M model (~1.5GB) automatically — that request will
be slow the first time, then fast afterwards since it's cached.

## 5. Project structure

```
EduGenie/
├── main.py                  # FastAPI app + routes
├── gemini_client.py         # Shared Gemini SDK setup
├── qna.py                   # Question answering
├── explanation_module.py    # Concept explanation (local model)
├── quiz_module.py           # Quiz generation
├── summary_module.py        # Summarization
├── learning_path.py         # Learning path recommendations
├── templates/index.html     # Frontend
├── static/style.css         # Styling
├── requirements.txt
├── .env.example
└── README.md
```

## Optional: skip the local model

If you don't want to install `torch`/`transformers` right now, you
can temporarily make `explain_concept` call Gemini instead:

1. Remove `transformers`, `torch`, `sentencepiece`, `accelerate` from
   `requirements.txt`.
2. Replace the body of `explanation_module.py` with a Gemini call
   identical in shape to `summary_module.py`, just with an
   "explain this simply" prompt instead of a summarization prompt.

This trades the "runs fully offline/local" benefit described in the
project doc for a much lighter install — useful while you're still
building and testing the rest of the app.

## Troubleshooting

- **`RuntimeError: GEMINI_API_KEY is missing`** — you forgot to
  create `.env` from `.env.example`, or didn't paste a real key.
- **Quiz returns a JSON parsing error occasionally** — this happens
  if Gemini's output isn't perfectly formed JSON. `quiz_module.py`
  already strips markdown code fences; if it still fails, try a
  shorter/clearer passage, or lower `temperature` isn't currently
  set — you can add `generation_config={"temperature": 0.4}` to the
  `generate_content()` call in `quiz_module.py` for more consistent
  output.
- **First "Explain" request is very slow** — expected, it's
  downloading the local model. Subsequent requests are fast.
