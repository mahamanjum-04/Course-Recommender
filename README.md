# Personalized Course Recommender

A Streamlit app that generates a real, field-specific skill test on the fly using an LLM (Mistral 7B), scores the user on correctness across five skill dimensions, and recommends real Coursera courses matched to where the user actually stands — prioritizing their weakest areas and gating course difficulty by their current competency level.

## What it does

1. **Pick a field** — AI & Machine Learning, Web Development, Data Science, Cybersecurity, or Mobile App Development.
2. **Take a skill test** — Mistral 7B generates 30 multiple-choice questions (6 per skill dimension: Programming, Aptitude, Technical, Problem Solving, Communication), ordered easy → medium → hard within each dimension, with no repeats across retakes.
3. **See your results** — a radar chart of your profile across all five dimensions, a gauge of your overall score, and a Low/Medium/High competency level.
4. **Get course recommendations** — the top matches are chosen using TF-IDF + cosine similarity, weighted toward your *weakest* dimensions (so recommendations target growth areas, not what you're already good at) and gated by your competency level (a Low-level user won't be pushed Advanced-only courses).

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your data files
Place these in the `data/` folder:
- `coursera_courses.csv` — **required**, the main course catalog
- `coursera_free_courses.csv` — optional, the app runs fine without it but recommendations will only draw from the main catalog

### 3. Set your Mistral API key
Get a free key at [console.mistral.ai](https://console.mistral.ai). Either:
- Create a `.env` file in the project root:
  ```
  MISTRAL_API_KEY=your-key-here
  ```
- Or enter it directly in the app when prompted (home page, if no key is detected).

Without a key, the app still runs — it falls back to a small built-in question bank instead of generating fresh questions, so it never crashes, it just won't be field-specific or varied.

### 4. Run it
```bash
streamlit run app.py
```
Run this from the project root — the internal imports (`from config.settings import ...`, etc.) only resolve correctly from there.

## Project structure

```
course-recommender/
├── app.py                      # Entry point: wires everything together, routes pages
├── .env                        # MISTRAL_API_KEY (not committed to version control)
├── .streamlit/config.toml      # Streamlit's native theme base
├── requirements.txt
├── README.md
│
├── config/
│   └── settings.py             # Fields, dimensions, difficulty split, colors, thresholds
│
├── data/
│   ├── loader.py                # Loads + merges the paid and free course datasets
│   └── coursera_*.csv           # Your data files
│
├── llm/
│   ├── client.py                # Mistral API client setup
│   ├── prompts.py                # Prompt templates for question generation
│   ├── questions.py              # Question generation, validation, retry logic
│   └── links.py                  # Best-effort AI link lookup for courses missing a URL
│
├── engine/
│   ├── scoring.py                # Dimension/overall scoring, competency level
│   └── recommendations.py        # TF-IDF + cosine similarity recommendation engine
│
├── ui/
│   ├── pages.py                  # Home, test, and results page rendering
│   ├── components.py             # Course cards, dimension breakdown table
│   ├── charts.py                 # Radar and gauge charts
│   └── theme.py                  # Light/dark mode CSS, typography, theme toggle
│
└── utils/
    └── helpers.py                # Session state init, page navigation, styling helpers
```

## How the core algorithms work

**Question generation** — for each of the 5 dimensions, a structured prompt asks Mistral 7B for 6 MCQs (2 easy, 2 medium, 2 hard) specific to the chosen field, returned as strict JSON with one correct answer each. Output is validated (4 options, valid answer index, correct difficulty split) and retried once if malformed; falls back to a small offline question bank if generation fails entirely.

**Scoring** — straightforward: `correct answers ÷ total answers × 100` per dimension, averaged for an overall score. Competency level (Low / Medium / High) is assigned via fixed score thresholds.

**Recommendations** — courses' `Skills` text is vectorized with **TF-IDF**; the user's profile (field keywords + their weakest dimensions, weighted by how weak they are) is vectorized the same way; **cosine similarity** ranks courses by topical closeness to that profile. Scores are then adjusted: bonus for difficulty matching the user's level, penalty if a Low-level user is looking at an Advanced course, small bonus for highly-rated courses.

**Course links** — used directly from the dataset when present; if missing, a second Mistral call attempts to recall a plausible URL, always labeled "AI-suggested, may not be accurate" since this is unverified model recall, not a live search.

## Known limitations (documented, not hidden)

- **No independent answer verification** — the model both writes each question and declares its own correct answer in the same call.
- **Competency thresholds are fixed**, not benchmarked against any real population data.
- **AI-suggested course links are unverified** — Mistral has no browsing tool here, so a guessed link can be wrong or outdated.
- **Small-model limits in testing** — persona-based testing showed Mistral 7B struggles to reliably roleplay "someone who doesn't know this material," since the model still knows the right answer from training. Deterministic tests (forcing known correct/incorrect answer patterns) are the more reliable way to verify scoring and recommendation logic; persona-based tests are better understood as a robustness/stress test than a correctness proof.

