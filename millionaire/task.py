import random

class Task:
    FIRST_SYM_CODE = ord('A')

    def __init__(self, question, answers, sum):
        self.question = question
        self.sum = sum
        answers = list(map(format, answers))
        self.correct_answer = answers[0]
        self.answers = {}
        for index, answer in enumerate(random.sample(answers, len(answers))):
            self.answers[chr(self.FIRST_SYM_CODE + index)] = answer

    def __str__(self):
        return self.sum_str() + self.question_str() + self.answers_str()

    def solved(self, answer):
        return self.correct_answer == answer

    def validate_answer_key(self, answer_key):
        return(self.answers[answer_key] if answer_key in self.answers else False)

    def question_str(self):
        return f"\n\n=== {self.question} ===\n\n"

    def sum_str(self):
        return f"Возможный выигрыш: {self.sum} рублей"

    def answers_str(self):
        str = 'Варианты ответов:'

        for key in self.answers:
            str += f"\n{key}. {self.answers[key]}"

        return str

    def format(item):
        return str(item).strip()
