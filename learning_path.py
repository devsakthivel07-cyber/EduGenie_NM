"""
learning_path.py
----------------
Generates a detailed, personalized, structured learning path
for a given topic: beginner -> intermediate -> advanced.
"""

from gemini_client import get_model


def get_learning_recommendations(topic: str) -> str:
    """
    Return a detailed beginner-to-advanced learning path for `topic`.
    """

    if not topic or not topic.strip():
        return "Please provide a topic to build a learning path for."

    model = get_model()

    prompt = f"""
You are an expert educational planner and mentor.

Create a DETAILED, practical, beginner-to-advanced learning roadmap
for the topic:

"{topic.strip()}"

The learner wants to genuinely learn this topic, not just receive
a short list of topics.

IMPORTANT:
- Give a detailed explanation.
- Do NOT give a very short answer.
- Do NOT reduce the roadmap to only a few bullet points.
- Cover the topic progressively from fundamentals to advanced concepts.
- Make the roadmap practical and suitable for self-study.
- Use clear Markdown formatting.
- Do not invent fake URLs, courses, books, or resources.
- When suggesting resources, describe them generically unless you are
  certain about the resource name.

Structure the response exactly around the following sections.

# Learning Roadmap: {topic.strip()}

## 1. What is {topic.strip()}?

Give a simple introduction explaining:
- What it is
- Why it is useful
- Where it is commonly used
- What the learner will be able to do after learning it

## 2. Prerequisites

List the knowledge or skills that should be known before starting.

For each prerequisite, briefly explain why it is useful.

## 3. Beginner Level

Explain the beginner stage in detail.

Include:
- Core concepts
- Important terminology
- Fundamental skills
- What the learner should understand
- Small practical exercises
- A beginner project or practice task

For every major concept, give a short explanation rather than
only naming the concept.

## 4. Intermediate Level

Explain the intermediate stage in detail.

Include:
- Important concepts
- Practical techniques
- Common patterns or approaches
- What the learner should be able to build or solve
- Practice exercises
- At least one intermediate project

Explain how this stage builds on the beginner level.

## 5. Advanced Level

Explain the advanced stage in detail.

Include:
- Advanced concepts
- Optimization or best practices where applicable
- Real-world techniques
- Common challenges
- Professional-level skills
- At least one advanced project

Explain what makes these topics advanced.

## 6. Recommended Learning Order

Give a numbered sequence showing the recommended order.

Example:

1. Foundation
2. Core concepts
3. Practical skills
4. Intermediate concepts
5. Projects
6. Advanced concepts
7. Real-world practice

Adapt the sequence specifically to the requested topic.

## 7. Practice Projects

Suggest at least 5 projects.

Organize them as:

### Beginner Projects
- Project name
- What it teaches
- Main concepts involved

### Intermediate Projects
- Project name
- What it teaches
- Main concepts involved

### Advanced Projects
- Project name
- What it teaches
- Main concepts involved

## 8. Suggested Resources

Suggest useful resource TYPES such as:
- Documentation
- Video tutorials
- Articles
- Books
- Practice websites
- Official documentation

For each resource type, explain what the learner should look for.

Do NOT invent URLs.

## 9. Estimated Timeline

Provide a realistic approximate timeline.

Break it into:
- Beginner
- Intermediate
- Advanced
- Projects/practice

Give estimates in weeks rather than unrealistic exact promises.

## 10. Common Mistakes to Avoid

List important mistakes beginners commonly make when learning
this topic and briefly explain how to avoid them.

## 11. Final Learning Goal

Explain what the learner should be capable of doing after completing
the roadmap.

End with a short checklist of skills the learner should have gained.

Remember:
The final answer should be DETAILED enough to function as an actual
study roadmap. Prefer useful explanations over extremely short
bullet points.
"""

    try:
        response = model.generate_content(prompt)

        return response.text.strip()

    except Exception as e:
        return (
            f"Sorry, I couldn't generate a learning path right now. ({e})"
        )