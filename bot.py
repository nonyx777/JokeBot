import json
from difflib import get_close_matches
import sys
import random

"""
Release mode - learning from input disabled
Debug mode - learning from input enabled
"""


#.....
accuracy = 0.6
arguments = sys.argv

#list to choose response from
#if bot doesn't know what to say
responses = ["I'm not familiar with your game mate, Is that even english", "English please!", "Wait wait wait hold your horses, what?", "I have no idea what you're trying to say, My good sir"]

#python bot.py --release or python bot.py --debug
if(len(arguments) != 2 or (arguments[1] != "--release" and arguments[1] != "--debug")):
    raise SystemExit("invalid argument")



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
    matches = get_close_matches(user_question, questions, n=1, cutoff=accuracy)
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
            if arguments[1] == "--release":
                random_response = random.choice(responses)
                print(random_response)
            else:
                print(f"Joker: I don\'t know the answer to '{user_input}'. Can you provide an answer?")
                new_answer: str = input('Type the answer or "skip" to skip: ')


                if new_answer.lower() != "skip":
                    knowledge_base["question"].append({"question": user_input, "answer": new_answer})
                    save_knowledge_base("knowledge_base.json", knowledge_base)
                    print("Joker: Thank You! I learned a new response!")

if __name__ == "__main__":
    chatbot()