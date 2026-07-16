import json
import random
import os

QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), "questions.json")

with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
    _questions = json.load(f)


def get_random_question(category=None):
    """
    Returns a random question dict from the bank.
    If category is provided, filters to that category first.
    Valid categories: "Python", "SQL", "Machine Learning",
    "Deep Learning", "AI/NLP/Computer Vision"
    """
    pool = _questions
    if category:
        pool = [q for q in _questions if q["category"].lower() == category.lower()]

    if not pool:
        return None

    return random.choice(pool)


def get_all_categories():
    return sorted(set(q["category"] for q in _questions))