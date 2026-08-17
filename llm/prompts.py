"""All prompt text and prompt-building logic in one place."""

from config.settings import DIFFICULTY_SPLIT

SYSTEM_PROMPT = (
    "You are an expert technical assessment writer creating multiple-choice skill "
    "test questions for a course-recommendation app. Return ONLY valid JSON — no "
    "markdown code fences, no commentary before or after the JSON."
)

USER_PROMPT_TEMPLATE = """Field: {field}
Skill dimension being tested: {dimension}
What this dimension should test in this field: {focus}

Write exactly {n} multiple-choice questions that genuinely test this specific skill in this field:
exactly {easy_n} EASY, exactly {medium_n} MEDIUM, and exactly {hard_n} HARD questions.
Return them in this exact order: all easy questions first, then all medium, then all hard.

Requirements:
- Each question must have exactly one objectively correct answer (no opinions, no self-rating).
- Provide exactly 4 answer options per question.
- Do not repeat the meaning of any of these previously used questions: {avoid}
- Keep each question concise and quick to read.

Return a JSON array of exactly {n} objects, each shaped exactly like this:
{{"question": "...", "options": ["...", "...", "...", "..."], "correct_answer": 0, "difficulty": "easy"}}

"correct_answer" is the zero-based index into "options" of the single correct option.
"difficulty" must be exactly one of: "easy", "medium", "hard", matching the required counts above.
Return ONLY the JSON array, nothing else.
"""


def build_prompt(field, dimension, focus, n, avoid_texts):
    avoid_str = "; ".join(avoid_texts[-8:]) if avoid_texts else "none yet"
    return USER_PROMPT_TEMPLATE.format(
        field=field, dimension=dimension, focus=focus, n=n, avoid=avoid_str,
        easy_n=DIFFICULTY_SPLIT['easy'], medium_n=DIFFICULTY_SPLIT['medium'], hard_n=DIFFICULTY_SPLIT['hard'],
    )