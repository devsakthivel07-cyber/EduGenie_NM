"""
summary_module.py
-------------------
Summarizes long educational passages into concise, easy-to-review
versions using Gemini, while retaining the core information.
"""

from gemini_client import get_model


def summarize_text(passage: str) -> str:
    """
    Return a concise summary of the given passage.
    """
    if not passage or not passage.strip():
        return "Please provide some text to summarize."

    model = get_model()

    prompt = (
        "Summarize the following educational passage into a concise, "
        "clear version suitable for quick revision. Keep the core "
        "facts and remove redundancy. Do not add information that "
        "isn't in the original text.\n\n"
        f"Passage:\n{passage.strip()}\n\n"
        "Summary:"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Sorry, I couldn't generate a summary right now. ({e})"
