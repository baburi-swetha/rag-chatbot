import json
import os



CONFIG_PATH = os.path.join(
    "config",
    "metadata_rules.json"
)

with open(CONFIG_PATH, "r") as f:
    RULES = json.load(f)


def calculate_score(text, keywords):

    score = 0

    for keyword in keywords:

        if keyword.lower() in text:

            score += 1

    return score



def detect_metadata(filename, text):

    text = text.lower()

    metadata = {}



    best_department = "General"

    best_score = 0

    for department, keywords in RULES["departments"].items():

        score = calculate_score(text, keywords)

        if score > best_score:

            best_score = score

            best_department = department

    metadata["department"] = best_department


    best_category = "General"

    best_score = 0

    for category, keywords in RULES["categories"].items():

        score = calculate_score(text, keywords)

        if score > best_score:

            best_score = score

            best_category = category

    metadata["category"] = best_category

    metadata["filename"] = filename

    return metadata