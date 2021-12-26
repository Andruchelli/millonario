from millionaire.game_data import *

class Engine:
    def __init__(self, filename):
        self.game_data = GameData(filename)
        self.current_step = 0

    def start_game(self):
        print("Добро пожаловать на игру \"Кто хочет стать миллионером?\"")
        prize = self.next_question()
        print(f"Ваш выигрыш составил {prize} рублей. До новых встреч!")
        return prize

    def ask_user(self, task):
        accepted_choices = ', '.join(list(task.answers))
        user_answer = input(f"\nВаш ответ {accepted_choices} или Stop, если хотите прекратить игру: ").strip().upper()
        validated_answer = task.validate_answer_key(user_answer)
        return(validated_answer if validated_answer else self.ask_user(task))

    def next_question(self, t = 1):
        task = self.game_data.task_for(self.current_step)
        print(f"Количество оставшихся попыток: {t}")
        print(f"\nВопрос №{self.current_step + 1}")
        print(task)

        user_result = self.game_data.check_answer(self.ask_user(task),
                                                  task,
                                                  self.current_step)

        if user_result["status"] == "win":
            print("Это правильный ответ!")
            print("Вы победили!!!")
            return user_result["prize"]
        elif user_result["status"] == "next_step":
            print("Это правильный ответ!")
            self.current_step = user_result["step"]
            return self.next_question()
        elif user_result["status"] == "stop":
            print("Попробуйте в следующий раз.")
            return user_result["prize"]
        else:
            print("К сожалению, вы ошиблись.")
            print(f"Правильный ответ: {task.correct_answer}")
            return user_result["prize"]
