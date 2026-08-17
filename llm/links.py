"""Best-effort link lookup for recommended courses whose dataset row has
no URL. This is NOT a verified or browsed lookup -- it's the LLM's best
guess from training data, and any link it returns MUST be labeled as
AI-suggested/unverified wherever it's shown."""

from config.settings import MISTRAL_MODEL

LINK_PROMPT = """Give the most likely official course URL for this Coursera course.
Course name: {name}
Provider/University: {provider}

If you are not fully confident of the exact URL, give the most plausible
Coursera course or search URL for it. Respond with ONLY the URL, nothing
else -- no explanation, no markdown, no extra text.
"""


def find_course_link(client, course_name, provider):
    """Returns a best-guess URL string, or None if no client is available
    or the lookup fails/returns something that isn't a URL."""
    if client is None:
        return None
    try:
        prompt = LINK_PROMPT.format(name=course_name, provider=provider or "Unknown")
        response = client.chat.complete(
            model=MISTRAL_MODEL,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        url = response.choices[0].message.content.strip()
        if url.startswith("http://") or url.startswith("https://"):
            return url
        return None
    except Exception:
        return None