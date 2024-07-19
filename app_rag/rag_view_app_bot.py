import telebot #Импортируется библиотека telebot для работы с ботом Telegram.
from telebot import types #Импортируется модуль types из telebot для работы с типами данных Telegram.

from app_rag.rag_view_message_handler import MessageHandler #Импортируется класс MessageHandler из модуля 

class BotView: 

    def __init__(self, bot, message_handler : MessageHandler): #Метод инициализации, принимает  объект  бота  Telegram  и  обработчик  сообщений.
        self.message_handler = message_handler #Сохраняет  обработчик  сообщений  в  атрибуте  self.message_handler
        self.bot = bot # Сохраняет  объект  бота  Telegram  в  атрибуте  self.bot.
        self.setup_handlers() # Вызывает  метод  setup_handlers  для  установки  обработчиков  сообщений.

    def setup_handlers(self): #Метод  для  установки  обработчиков  сообщений.
        @self.bot.message_handler(commands=['start']) #Декоратор  для  обработки  команды  /start.
        def start_command(message): #Функция-обработчик  команды  /start.
            self.message_handler.handle_start(message) #Передает  сообщение  обработчику  сообщений  для  обработки  команды  /start.

        @self.bot.message_handler(commands=['help']) 
        def help_command(message):
            self.message_handler.handle_help(message)

        @self.bot.message_handler(func=lambda message: True) #Декоратор  для  обработки  всех  сообщений.
        def all_messages(message):
            self.message_handler.handle_message(message) #ередает  сообщение  обработчику  сообщений  для  обработки.

    def run(self): # Метод  для  запуска  бота  Telegram.
        self.bot.polling(non_stop=True) #Запускает  бот  в  режиме  опроса  (polling),  постоянно  проверяя  наличие  новых  сообщений.
