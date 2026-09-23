"""
quiz_module.py
---------------
Generates three multiple-choice questions (4 options each) from a
passage of text, using Gemini. Output is structured JSON so the
frontend can render it as an interactive quiz.
"""

import json
import re
from gemini_client import get_model


def clean_json_block(text: str) -> str:
    """
    Gemini sometimes wraps JSON in ```json ... ``` code fences.
    Strip those so json.loads() doesn't choke on them.
    """
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_quiz(passage: str):
    """
    Return a list of 3 question dicts, each shaped like:
    {
        "question": "...",
        "options": ["A", "B", "C", "D"],
        "answer": "the correct option text"
    }
    On failure, returns a dict with an "error" key instead.
    """
    if not passage or not passage.strip():
        return {"error": "Please provide a passage or topic to quiz on."}

    model = get_model()

    prompt = (
        "You are a quiz generator for a learning app. Based on the "
        "passage below, create exactly 3 multiple-choice questions. "
        "Each question must have exactly 4 options, and one of them "
        "must be the correct answer. The distractors should be "
        "plausible but clearly wrong on reflection.\n\n"
        "Return ONLY valid JSON — no explanation, no markdown — in "
        "exactly this shape:\n"
        "[\n"
        "  {\n"
        '    "question": "string",\n'
        '    "options": ["string", "string", "string", "string"],\n'
        '    "answer": "string (must exactly match one of the options)"\n'
        "  }\n"
        "]\n\n"
        f"Passage:\n{passage.strip()}"
    )

    try:
        response = model.generate_content(prompt)
        cleaned = clean_json_block(response.text)
        quiz = json.loads(cleaned)

        # sanity-check the shape before handing it to the frontend
        if not isinstance(quiz, list) or len(quiz) == 0:
            raise ValueError("Model did not return a list of questions.")
        for q in quiz:
            if not all(k in q for k in ("question", "options", "answer")):
                raise ValueError("A question is missing required fields.")
            if len(q["options"]) != 4:
                raise ValueError("A question does not have 4 options.")

        return quiz

    except json.JSONDecodeError as e:
        return {"error": f"Could not parse quiz JSON from the model. ({e})"}
    except Exception as e:
        return {"error": f"Sorry, quiz generation failed. ({e})"}
