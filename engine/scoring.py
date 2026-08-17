"""Scoring: correctness-based dimension scores, overall score, and
competency-level labeling."""

import numpy as np
from config.settings import SCORE_THRESHOLDS


def calculate_dimension_scores(responses, questions):
    correct_counts, total_counts = {}, {}
    for i, response in enumerate(responses):
        if i >= len(questions):
            continue
        dim = questions[i]['dimension']
        total_counts[dim] = total_counts.get(dim, 0) + 1
        if response is not None and response == questions[i]['correct_answer']:
            correct_counts[dim] = correct_counts.get(dim, 0) + 1
    return {dim: (correct_counts.get(dim, 0) / total) * 100 for dim, total in total_counts.items()}


def calculate_overall_score(dim_scores):
    return np.mean(list(dim_scores.values())) if dim_scores else 0


def get_competency_level(score):
    if score < SCORE_THRESHOLDS['low']:
        return "Low"
    elif score < SCORE_THRESHOLDS['medium']:
        return "Medium"
    return "High"