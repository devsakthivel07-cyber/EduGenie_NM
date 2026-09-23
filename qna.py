"""
qna.py
------
Handles general question-answering using Gemini 1.5 Pro.
Scenario from the project doc: "A student asks 'Which is the
largest ocean?'" -> this module returns a smart, concise answer.
"""

from gemini_client import get_model


def answer_question(question: str) -> str:
    """
    Send a student's question to Gemini and return a concise,
    easy-to-understand answer.
    """
    if not question or not question.strip():
        return "Please enter a question."

    model = get_model()

    prompt = (
        "You are EduGenie, a friendly educational assistant. "
        "Answer the student's question accurately and concisely. "
        "Keep it clear enough for a school or college student to "
        "understand quickly.\n\n"
        f"Question: {question.strip()}\n\n"
        "Answer:"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Sorry, I couldn't generate an answer right now. ({e})"
