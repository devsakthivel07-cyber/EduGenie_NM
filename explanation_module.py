"""
explanation_module.py
----------------------
Concept explanation using LaMini-Flan-T5-783M.

The model runs locally on CPU, so concept explanations do not
require a Gemini API call.
"""

from functools import lru_cache
from transformers import pipeline

_MODEL_NAME = "MBZUAI/LaMini-Flan-T5-783M"


@lru_cache(maxsize=1)
def _get_pipeline():
    """
    Load the model once and reuse it across requests.
    """

    return pipeline(
        "text2text-generation",
        model=_MODEL_NAME,
        max_new_tokens=600,
    )


def explain_concept(topic: str) -> str:
    """
    Return a detailed, beginner-friendly explanation of a concept.
    """

    if not topic or not topic.strip():
        return "Please enter a topic to explain."

    topic = topic.strip()

    prompt = f"""
You are a patient computer science teacher.

Explain the following concept to a college student who is a beginner:

Topic: {topic}

Give a detailed but easy-to-understand explanation.

Use the following structure:

1. Definition
Explain what {topic} is in simple words.

2. Why It Is Important
Explain why this concept is useful and where it is used.

3. Basic Idea
Explain the main idea behind the concept step by step.

4. How It Works
Describe how it works in a simple sequence of steps.

5. Simple Example
Give a small and easy example related to the concept.

6. Real-World Example
Give one practical real-world application.

7. Important Points
List the important points a student should remember.

8. Common Mistakes
Mention common misunderstandings or mistakes beginners may make.

9. Quick Recap
End with a short summary of the concept.

Rules:
- Use simple English.
- Explain concepts instead of only listing them.
- Use short paragraphs and bullet points where useful.
- Do not assume advanced knowledge.
- Avoid unnecessary technical jargon.
- If a technical term is necessary, explain it.
- Make the explanation educational and detailed.
"""

    try:
        generator = _get_pipeline()

        result = generator(
            prompt,
            max_new_tokens=600,
            do_sample=True,
            temperature=0.7,
        )

        return result[0]["generated_text"].strip()

    except Exception as e:
        return (
            f"Sorry, I couldn't generate an explanation right now. ({e})"
        )