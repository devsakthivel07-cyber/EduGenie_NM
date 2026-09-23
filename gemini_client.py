"""
gemini_client.py
-----------------
Central place that configures the Google Gemini SDK once and hands
back a ready-to-use model object. Every module that needs Gemini
(qna, quiz_module, summary_module, learning_path) imports get_model()
from here instead of configuring the SDK itself.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # reads .env in the project root

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY or API_KEY == "your_gemini_api_key_here":
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Copy .env.example to .env and paste "
        "your real key from https://aistudio.google.com/app/apikey"
    )

genai.configure(api_key=API_KEY)

# "gemini-1.5-pro" per the project doc. Swap to "gemini-1.5-flash"
# if you want faster/cheaper responses during development.
_MODEL_NAME = "gemini-3.5-flash"

_model = genai.GenerativeModel(_MODEL_NAME)


def get_model():
    """Return the shared Gemini model instance."""
    return _model
