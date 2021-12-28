import yaml
import random
from millionaire.task import *

class GameData:
    def __init__(self, filename):
        self.tasks = self.load_tasks_from(filename)
        self.steps = self.get_steps_for(self.tasks)
        self.total_steps = len(self.steps)

    def check_answer(self, user_answer, task, step, t):
        result = {}
        if task.solved(user_answer) and (step + 1) == self.total_steps:
            result["status"] = "win"
            result["prize"] = self.steps[step]
        elif task.solved(user_answer) and (step + 1) != self.total_steps:
            result["status"] = "next_step"
            result["step"] = step + 1
        elif user_answer != task.correct_answer and t > 0:
            result["status"] = "retry"
            result["step"] = step
            result["prize"] = self.steps[step]
        elif user_answer != task.correct_answer and t == 0:
            result["status"] = "loss"
            result["prize"] = 0 if step == 0 else self.steps[step - 1]
        elif user_answer == "Stop":
            result["status"] = "stop"
            result["prize"] = 0 if step == 0 else self.steps[step - 1]

        return result

    def task_for(self, step):
        sum = self.steps[step]
        return random.choice(self.tasks[sum])

    def load_tasks_from(self, filename):
        try:
            file = open(filename, 'r', encoding="utf8")
            raw_data = yaml.safe_load(file.read())
            tasks = {}
            for sum, raw_tasks in raw_data.items():
                tasks.setdefault(sum, [])
                for raw_task in raw_tasks:
                    task = Task(raw_task['question'], raw_task['answers'], sum)
                    tasks[sum].append(task)
        except FileNotFoundError:
            exit("Не удалось загрузить задания для игры!")
        except yaml.parser.ParserError:
            file.close()
            exit("Задания имеют некорректный формат!")
        else:
            file.close()
            return tasks

    def get_steps_for(self, tasks):
        steps = list(tasks)
        steps.sort()
        return steps
