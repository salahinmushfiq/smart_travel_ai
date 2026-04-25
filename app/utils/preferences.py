# app/utils/preferences.py

def extract_preferences(question: str):
    q = question.lower()
    tags = []

    if "hill" in q:
        tags.append("hill")
    if "beach" in q:
        tags.append("beach")
    if "city" in q:
        tags.append("city")
    if "nature" in q:
        tags.append("nature")

    return tags