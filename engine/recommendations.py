"""TF-IDF + cosine similarity course recommendation engine. Recommendations
are weighted toward the user's WEAKEST dimensions (their growth areas) and
gated by their overall skill level, so a beginner gets beginner-level
courses in the areas they most need to work on -- not advanced courses in
what they're already good at."""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config.settings import FIELDS, TOP_N_RECOMMENDATIONS
from engine.scoring import calculate_overall_score, get_competency_level

LEVEL_MAPPING = {
    'Low': ['beginner', 'mixed'],
    'Medium': ['intermediate', 'mixed'],
    'High': ['advanced', 'intermediate', 'mixed'],
}

# Course difficulty levels considered a poor fit for each user level --
# these get actively penalized, not just skipped for a bonus.
MISMATCH_PENALTY = {
    'Low': ['advanced'],
    'Medium': [],
    'High': [],
}


def get_course_recommendations(user_scores, field, courses_df, top_n=TOP_N_RECOMMENDATIONS):
    if courses_df is None or len(courses_df) == 0:
        return []

    df = courses_df.copy()
    df['Skills'] = df['Skills'].fillna('')

    sorted_dims_weakest_first = sorted(user_scores.items(), key=lambda x: x[1])
    weakest_dim = sorted_dims_weakest_first[0][0] if sorted_dims_weakest_first else None

    profile_terms = list(FIELDS[field]['keywords']) * 3
    for dim, score in sorted_dims_weakest_first:
        weight = max(1, round((100 - score) / 25))  # lower score -> more weight
        profile_terms.extend([dim.lower()] * weight)
    user_profile = ' '.join(profile_terms)

    corpus = df['Skills'].tolist() + [user_profile]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

    overall = calculate_overall_score(user_scores)
    user_level = get_competency_level(overall)

    recommendations = []
    for idx, sim in enumerate(similarities):
        course = df.iloc[idx]
        match_score = sim * 0.6
        reasons = []
        if sim > 0.1 and weakest_dim:
            reasons.append(f"Helps strengthen {weakest_dim} (your current growth area)")

        course_level = str(course.get('Difficulty', '')).lower() if pd.notna(course.get('Difficulty')) else ''
        if course_level:
            if any(l in course_level for l in LEVEL_MAPPING.get(user_level, [])):
                match_score += 0.3
                reasons.append(f"Suitable for your current {user_level.lower()} level")
            elif any(l in course_level for l in MISMATCH_PENALTY.get(user_level, [])):
                match_score -= 0.25
                reasons.append(f"⚠️ May be too advanced for your current {user_level.lower()} level")

        if pd.notna(course.get('Rating')):
            try:
                rating = float(course['Rating'])
                if rating >= 4.5:
                    match_score += 0.15
                    reasons.append("Highly rated")
                elif rating >= 4.0:
                    match_score += 0.1
            except (ValueError, TypeError):
                pass

        match_score = max(0.0, min(1.0, match_score))
        if match_score > 0.05:
            recommendations.append({'course': course, 'match_score': match_score, 'reasons': reasons[:3]})

    recommendations.sort(key=lambda x: x['match_score'], reverse=True)
    return recommendations[:top_n]