"""Question generation: turns a field + dimension into real MCQs via the
Mistral API, with retry-on-malformed-output/wrong-difficulty-split and a
safe offline fallback."""

import json
import random
from collections import Counter

from config.settings import FALLBACK_QUESTIONS, MISTRAL_MODEL, FIELDS, N_PER_DIMENSION, DIFFICULTY_SPLIT
from llm.prompts import SYSTEM_PROMPT, build_prompt

DIFFICULTY_ORDER = {'easy': 0, 'medium': 1, 'hard': 2}


def _fallback_for(dimension, n):
    bank = FALLBACK_QUESTIONS[dimension]
    selected = (bank * ((n // len(bank)) + 1))[:n]
    return [dict(q, dimension=dimension) for q in selected]


def generate_dimension_questions(client, field, dimension, focus, n, avoid_texts):
    """Generate n questions for one dimension, ordered easy -> hard with the
    exact difficulty split from DIFFICULTY_SPLIT. Returns (questions, used_fallback)."""
    if client is None:
        return _fallback_for(dimension, n), True

    prompt = build_prompt(field, dimension, focus, n, avoid_texts)

    import time
    for attempt in range(2):  # one retry on malformed output or wrong difficulty split
        if attempt > 0:
            time.sleep(2)  # brief backoff in case the first failure was a rate limit
        try:
            response = client.chat.complete(
                model=MISTRAL_MODEL,
                temperature=0.9,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
            )
            raw = response.choices[0].message.content.strip().strip('`')
            if raw.lower().startswith('json'):
                raw = raw[4:].strip()
            data = json.loads(raw)

            questions = []
            for item in data[:n]:
                opts = item.get('options')
                ca = item.get('correct_answer')
                difficulty = item.get('difficulty', 'medium')
                if difficulty not in DIFFICULTY_ORDER:
                    difficulty = 'medium'
                if (isinstance(opts, list) and len(opts) == 4
                        and isinstance(ca, int) and 0 <= ca <= 3
                        and item.get('question')):
                    questions.append({
                        'question': item['question'],
                        'options': opts,
                        'correct_answer': ca,
                        'dimension': dimension,
                        'difficulty': difficulty,
                    })

            if len(questions) == n:
                counts = Counter(q['difficulty'] for q in questions)
                if all(counts.get(level, 0) == required for level, required in DIFFICULTY_SPLIT.items()):
                    questions.sort(key=lambda q: DIFFICULTY_ORDER[q['difficulty']])
                    return questions, False
                # wrong split -> fall through to retry
        except Exception:
            continue

    return _fallback_for(dimension, n), True


def generate_full_test(client, field, n_per_dimension=N_PER_DIMENSION):
    """Generate the full test across all 5 dimensions. Each dimension's
    questions stay in easy-to-hard order; only the order the dimensions
    themselves appear in is randomized."""
    all_questions = []
    used_texts = []
    any_fallback = False
    dims = list(FIELDS[field]['focus'].items())
    random.shuffle(dims)
    for dimension, focus in dims:
        qs, fell_back = generate_dimension_questions(client, field, dimension, focus, n_per_dimension, used_texts)
        any_fallback = any_fallback or fell_back
        used_texts.extend(q['question'] for q in qs)
        all_questions.extend(qs)
    return all_questions, any_fallback