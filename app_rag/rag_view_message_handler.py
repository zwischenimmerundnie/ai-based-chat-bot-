import telebot # Импортирует библиотеку telebot для работы с API Telegram
import re # Импортирует библиотеку re для работы с регулярными выражениями
from telebot import types   # Импортирует класс types для создания кнопок и клавиатур

from app_rag.rag_presenter_app_bot import BotPresenter # Импортирует класс BotPresenter для работы с GPT-моделью

message_error = "Что-то пошло не так...\n\nПопробуйте перезапустить бота /start. Если проблема повторится, свяжитесь с автором\n @sams3pi01" # Ошибка, которая будет отображаться при возникновении проблем
class MessageHandler: # Класс для обработки сообщений

    def __init__(self, bot, presenter: BotPresenter):  # Инициализатор класса
        self.bot = bot # Сохраняет ссылку на объект бота
        self.presenter = presenter  # Сохраняет ссылку на объект BotPresenter
        self.gif_message_id = None # Инициализирует переменную для хранения ID GIF-сообщения

    def handle_start(self, message):  # Обработчик команды /start
        keyboard = types.ReplyKeyboardMarkup() # Создает клавиатуру
        button2 = types.KeyboardButton("Настроить актуальность 📅") # Создает кнопку "Настроить актуальность"
        keyboard.add(button2)  # Добавляет кнопку на клавиатуру
        self.bot.reply_to( # Отправляет сообщение в ответ на команду /start
            message,
            "👋 Привет! 你好！\n\nЯ твой ассистент по китайским СМИ. \n\nЯ умею читать новости на китайском и извлекать из них нужную информацию.\n\nГотов попытаться ответить на интересующие тебя вопросы по китайским СМИ!",
            reply_markup=keyboard,  # Прикрепляет клавиатуру к сообщению
        )

    def handle_message(self, message):  # Обработчик обычных сообщений
        if "Настроить актуальность" in message.text: # Проверяет, содержит ли сообщение фразу "Настроить актуальность"
            self.choose_period(message) # Вызывает метод для выбора периода
        else:
            try:
                self.bot.reply_to(message, "Дайте подумать...\n\n" + message.text) # Отправляет сообщение "Дайте подумать..."
                self.send_waiting_gif(message) # Отправляет GIF-анимацию
                gpt_response = self.presenter.send_query(message.text) # Отправляет запрос GPT-модели
                # escaped_response = self.escape_markdown_v2(gpt_response) # Экранирует ответ GPT-модели (не используется в данном коде)
                self.delete_gif_message(message) # Удаляет GIF-анимацию
                self.bot.reply_to(message, gpt_response) # Отправляет ответ GPT-модели
            except Exception as ex: # Обрабатывает исключения
                print(ex)  # Выводит ошибку в консоль
                self.bot.reply_to(message, message_error) # Отправляет сообщение об ошибке

    def escape_markdown_v2(self, text):  # Метод для экранирования текста
        escape_chars = r'\_*[]()~`>#+-=|{}.!' # Список символов, которые нужно экранировать
        return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text) # Экранирует символы в тексте
    
    def start_discussion(self, message): # Метод для начала нового диалога (не используется в данном коде)
        # Placeholder for starting a new dialog with context saving
        self.bot.reply_to(
            message, "Начато новое обсуждение 📝. (Контекст будет сохранен.)"
        )

    def choose_period(self, message): # Метод для выбора периода
        # Placeholder for handling period selection
        self.bot.reply_to(message, "Введите год из диапазона 2016-2023:") # Просит пользователя ввести год
        self.bot.register_next_step_handler(message, self.get_year) # Регистрирует обработчик для следующего сообщения

    def get_year(self, message): ## Обработчик сообщения с годом
        try:
            period = int(message.text) # Преобразует введенный текст в число
            self.presenter.period = period # Устанавливает период в объект BotPresenter
            self.bot.reply_to(message, f"Год: {period} установлен! Весь контекст будет не позже {period} года.") # # Отправляет сообщение об успешном установлении периода
        except Exception as ex:  # Обрабатывает исключения
            print(ex)  # Выводит ошибку в консоль
            self.bot.reply_to(message, f"Хм...\n\nЭто не похоже на число.") # Отправляет сообщение о том, что введен неправильный год

    def handle_help(self, message): #Обработчик команды /help
        self.bot.send_message(  # Отправляет сообщение с доступными командами
            message.chat.id, "Доступные команды: /start, /help", parse_mode="html"
        )

    def send_waiting_gif(self, message): # Метод для отправки GIF-анимации
        # Sending a GIF file to the user while waiting for GPT response
        gif_path = "/app/app_rag/sources/tom-ching-cheng-hanji.gif"  # Update with the actual path to your GIF file #Путь к файлу GIF (нужно заменить на правильный путь)
        with open(gif_path, "rb") as gif: # Открывает файл GIF для чтения в двоичном режиме
            sent_message = self.bot.send_animation(message.chat.id, gif)  # Отправляет GIF-анимацию пользователю
            self.gif_message_id = (  # Сохраняет ID отправленного сообщения
                sent_message.message_id
            )  # Store the message ID of the sent GIF

    def delete_gif_message(self, message): # Метод для удаления GIF-анимации
        if self.gif_message_id: # Проверяет, есть ли ID GIF-сообщения
            self.bot.delete_message(
                chat_id=message.chat.id, message_id=self.gif_message_id
            ) # Удаляет GIF-сообщение
            self.gif_message_id = None # Сбрасывает ID GIF-сообщения
