import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    try:
        with open(file_path, "r") as file:
            data: dict = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {"question": []}

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file)

def find_best_match(user_question: str, questions: list[str]) -> str| None:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.3)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str:
    for q in knowledge_base["question"]:
        if q["question"] == question:
            return q["answer"]
        
def chatbot():
    knowledge_base: dict = load_knowledge_base("knowledge_base.json")

    while True:
        user_input: str = input("You: ").lower()

        if user_input.lower() == "quit":
            break

        best_match: str| None = find_best_match(user_input, [q["question"] for q in knowledge_base["question"]])
        
        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f"Joker: {answer}")
        else:
            print(f"Joker: I don\'t know the answer to '{user_input}'. Can you provide an answer?")
            new_answer: str = input('Type the answer or "skip" to skip: ')


            if new_answer.lower() != "skip":
                knowledge_base["question"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base("knowledge_base.json", knowledge_base)
                print("Joker: Thank You! I learned a new response!")

if __name__ == "__main__":
    chatbot()