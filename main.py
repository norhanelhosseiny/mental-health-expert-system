import tkinter as tk
from tkinter import messagebox

from experta import Fact

from production_rules import MentalHealthAssessment
from questions_data import questions_by_level

class MentalHealthGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mental Health Assessment Expert System")
        self.level = 1
        self.answers = {}

        self.engine = MentalHealthAssessment()
        self.engine.reset()

        self.question_label = tk.Label(root, text="", wraplength=400)
        self.question_label.pack(pady=10)

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.next_button = tk.Button(root, text="Next", command=self.next_question)
        self.next_button.pack(pady=10)

        self.current_question_index = 0
        self.show_question()

    def show_question(self):
        if self.level > 8:
            self.submit_answers()
            return

        questions = questions_by_level[self.level]
        if self.current_question_index < len(questions):
            question_text, _ = questions[self.current_question_index]
            self.question_label.config(text=f"Level {self.level}: {question_text}")
        else:
            self.level += 1
            self.current_question_index = 0
            self.show_question()

    def next_question(self):
        answer = self.entry.get().strip()
        if answer == "":
            messagebox.showwarning("Warning", "Please enter an answer.")
            return

        key = questions_by_level[self.level][self.current_question_index][1]
        self.answers[key] = answer
        self.entry.delete(0, tk.END)
        self.current_question_index += 1
        self.show_question()

    def submit_answers(self):
        for key, value in self.answers.items():
            self.engine.declare(Fact(**{key: value}))

        self.engine.run()

        result = "\n\n".join(self.engine.diagnoses)


        result += "\n\nThis assessment is not a medical diagnosis. For a full evaluation, consult a licensed mental health professional."

        messagebox.showinfo("Diagnosis Result", result)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    gui = MentalHealthGUI(root)
    root.mainloop()
