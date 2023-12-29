import json
from difflib import get_close_matches
import sys
import random

import tkinter.messagebox
from tkinter.simpledialog import askstring
import customtkinter

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

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("JokeBot")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="JOKER", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.sidebar_button_event("Release"), text="Release Mod")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.sidebar_button_event("Debug"), text="Debug Mod")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Type your question here...", width=50, height=30)
        self.entry.grid(row=3, column=1, padx=(20, 10), pady=(20, 20), sticky="nsew")
        self.entry.bind("<Return>", lambda event: self.send_button_event())

        self.send_button = customtkinter.CTkButton(self, text="Send", command=self.send_button_event)
        self.send_button.grid(row=3, column=2, padx=(0, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=600, height=600)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.textbox.insert("10.0", "")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self, mode):
        global arguments

        if mode == "Release":
            arguments[1] = "--release"
        elif mode == "Debug":
            arguments[1] = "--debug"

        print(f"Switching to {arguments[1]} mode")

    def send_button_event(self):
        user_input = self.entry.get().strip()

        if not user_input:
            return  # Do nothing if the user input is empty

        if user_input.lower() == "quit" or user_input.lower() == "exit":
            self.quit()
            return

        # Display user's input in the textbox
        self.textbox.insert("end", f"You: {user_input}\n\n", ("user",))

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["question"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            response = f"Joker: {answer}"
        else:
            response = f"Joker: I don\'t know the answer to '{user_input}'. Can you provide an answer?"
            new_answer = askstring("Provide Answer", "Type the answer or click Cancel to skip:")

            if new_answer is not None:
                knowledge_base["question"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base("knowledge_base.json", knowledge_base)
                response = "Joker: Thank You! I learned a new response!"
            else:
                response = "Joker: Okay, let me know if you have another question."

        # Display chatbot's response in the textbox
        self.textbox.insert("end", f"{response}\n\n", ("joker",))

        # Clear the entry widget
        self.entry.delete(0, 'end')


if __name__ == "__main__":
    knowledge_base = load_knowledge_base("knowledge_base.json")

    app = App()
    app.mainloop()