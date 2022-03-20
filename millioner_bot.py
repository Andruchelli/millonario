# token для бота: 5298096408:AAFJuZ7--wjINGc9yVjdsU_Exrh3QLqrCNI

import logging
import random
from telegram.ext import Updater
from telegram.ext import CommandHandler # модуль для реагирования на команды, отдаваемые пользователем (команды записываются через "/")
from telegram.ext import MessageHandler # модуль для реагирования на сообщения
from telegram.ext import Filters # модуль для фильтрации сообщений
import urllib.parse # модуль parse библиотеки urllib для кодирования кириллицы в латиницу
import urllib.request # модуль для отправки запроса на сервер
import sys
from millionaire.engine import Engine

class Bot:
    def __init__(self, token): # метод
         print("Загрузка...")
         self.enable_logging() # журналирование - вывод сообщений при сбоях в программе
         self.updater = Updater(token=token, use_context=True) # updater для получения обновлений из телеграма (например, реагировать на команды, которые отдаёт пользователь, написав в чат)
         self.dispatcher = self.updater.dispatcher
         self.add_handlers() # метод для создания новых обработчиков для возникающих событий (получение сообщений или команд)

    def work(self): # метод для запуска бота, когда он готов к работе
        self.updater.start_polling() # для для запрашивания обновлений из телеграма
        print("Бот готов к работе")
        self.updater.idle() # в этом случае бот будет запущен в терминале до тех пор, пока не сработает комбинация клавиш Ctrl + C или Ctrl + Break

    def enable_logging(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - % (message)s', level=logging.INFO) # в рамках данного метода выводится сообщение в формате: время, название события, уровень события (инф. сообщение/ошибка), сообщение, которое необходимо вывести. Уровень протоколирования = INFO (вывод начинается с информационных сообщений)

    def add_handlers(self): # метод для создания новых обработчиков для возникающих событий (получение сообщений или команд)
        start_handler = CommandHandler('start', self.start) # обработчик для команды /start
        # если пользователь введёт команду /start, то будет запущен метод self.start (отправится сообщение "Привет!")
        self.dispatcher.add_handler(start_handler) # добавляем обработчик в диспетчер

        msg_handler = MessageHandler(Filters.text & (~Filters.command), self.msg) # обработка сообщений, которые присылают пользователи;
        # фильтрация текста:
        # Filters.text & (~Filters.command) - означает вызывать обработчик только в том случае, если был прислан текст и не была прислана команда
        self.dispatcher.add_handler(msg_handler) # добавляем обработчик в диспетчер

        play_handler = CommandHandler('play', self.play) # обработчик для команды /play (начать игру)
        self.dispatcher.add_handler(play_handler) # добавляем обработчик в диспетчер

        unknown_handler = MessageHandler(Filters.command, self.unknown) # сообщение для ситуации, когда присланная инструкция непонятна (для всех сообщений, которые являются коммандами)
        # данный обработчик должен идти последним после всех остальных обработчиков комманд и сообщений
        self.dispatcher.add_handler(unknown_handler) # добавляем обработчик в диспетчер

    def play(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Добро пожаловать на игру \"Кто хочет стать миллионером?\"")
        engine = Engine('tasks.yml' if len(sys.argv) < 2 else sys.argv[1])
        prize = engine.start_game()
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ваш выигрыш составил {prize} рублей. До новых встреч!")
        return prize

    def start(self, update, context): # context - контекст выполнения команды; используется для того, чтобы, например, отправить сообщение в чат
        context.bot.send_message(chat_id=update.effective_chat.id, text="Привет!")
        # effective_chat.id - текущий чат
        # text - текст, который мы хотим отправить

    def msg(self, update, context):
        if update.message.text.lower() == "привет": # если прислано сообщение "Привет" (неважно в каком регистре из-за ф-ии lower, которая определяет слово со строчными буквами)
            text = "И тебе привет" # в ответ отправляется сообщение "И тебе привет"
        else:
            text = f"Я получил сообщение '{update.message.text}'. Не знаю, что ответить."

        context.bot.send_message(chat_id=update.effective_chat.id, text=text) # отправляем в чат сообщение (text), которое записали выше; так происходит обработка сообщения (ответ на сообщение пользователя)

    def unknown(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text= f"Не знаю, как обработать команду '{update.message.text}'.")

bot = Bot('5298096408:AAFJuZ7--wjINGc9yVjdsU_Exrh3QLqrCNI')
bot.work() # запуск бота
