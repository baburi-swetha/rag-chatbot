import json
import os

CONFIG_PATH = os.path.join("config", "metadata_rules.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    RULES = json.load(f)


def calculate_score(text, keywords):
    
    text = text.lower()
    score = 0

    for keyword in keywords:
        score += text.count(keyword.lower())

    return score


def classify_query(question):
    

    question = question.lower()

    result = {
        "department": "General",
        "category": "General"
    }

    best_department = "General"
    best_score = 0

    for department, keywords in RULES["departments"].items():
        score = calculate_score(question, keywords)

        if score > best_score:
            best_score = score
            best_department = department

    result["department"] = best_department


    best_category = "General"
    best_score = 0

    for category, keywords in RULES["categories"].items():
        score = calculate_score(question, keywords)

        if score > best_score:
            best_score = score
            best_category = category

    result["category"] = best_category

    return result


if __name__ == "__main__":

    while True:

        question = input("\nAsk a question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        prediction = classify_query(question)

        print("\nPredicted Metadata")
        print("-------------------")
        print(f"Department : {prediction['department']}")
        print(f"Category   : {prediction['category']}")
