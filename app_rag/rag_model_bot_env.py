"""Этот код реализует класс Config, который предоставляет методы для получения 
конфигурационных параметров приложения. Давайте разберем его по строкам:"""

import os #Модуль для работы с операционной системой.

import time #Модуль для работы со временем.
import jwt #Модуль для работы с JWT.
import requests #Модуль для отправки HTTP-запросов.
import time
import jwt
import json #Модуль для работы с JSON.

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('/app/.env')
#Функция из модуля dotenv для загрузки переменных окружения из файла .env.

#Загружает переменные окружения из файла .env, расположенного в каталоге /app.

class Config: #Определяет класс Config, который содержит статические методы для получения конфигурационных параметров.

    @staticmethod #Декоратор @staticmethod указывает на то, что эти методы не привязаны к конкретному объекту класса и могут быть вызваны напрямую с помощью имени класса.
    def get_telegram_bot_token(): # Эти методы получают значения конфигурационных параметров из переменных окружения, используя os.getenv(). Если переменная не найдена, возвращается пустая строка.
        return os.getenv('TELEGRAM_BOT_TOKEN', '')
    
    @staticmethod
    def get_api_key():
        return os.getenv('API_KEY', '')

    @staticmethod
    def load_token(): #Этот метод генерирует JWT (JSON Web Token) для аутентификации и записывает его в файл jwt_token.txt.
        with open('/app/.configs/authorized_key.json', 'r') as f: #Открывает файл authorized_key.json для чтения.
            obj = f.read() #Читает содержимое файла и преобразует его в JSON-объект
            obj = json.loads(obj) #Читает содержимое файла и преобразует его в JSON-объект
            private_key = obj['private_key'] #Извлекает из JSON-объекта необходимые значения: private_key, key_id и service_account_id.
            key_id = obj['id']
            service_account_id = obj['service_account_id']

        now = int(time.time()) #Получает текущее время в секундах.
        payload = { #Создает словарь с полезной нагрузкой для JWT, включающий аудиторию, издателя, время выпуска и время истечения.
                'aud': 'https://iam.{{ api-host }}/iam/v1/tokens',
                'iss': service_account_id,
                'iat': now,
                'exp': now + 3600
            }

        # Формирование JWT.  #Создает JWT, используя private_key, алгоритм PS256 и заголовок, содержащий kid.
        encoded_token = jwt.encode(
            payload,
            private_key,
            algorithm='PS256',
            headers={'kid': key_id}
        )
        #Запись ключа в файл
        with open('jwt_token.txt', 'w') as j: #Записывает полученный JWT в файл jwt_token.txt.
            j.write(encoded_token) 
    
    @staticmethod
    def get_iam_token():  #Этот метод возвращает JWT из файла jwt_token.txt. Если файл не существует, он вызывает load_token() для создания нового JWT.
        if os.path.exists('/app/jwt_token.txt'):
            with open('/app/jwt_token.txt', 'r') as j:
                encoded_token = j.read()
            return encoded_token
        else:
            return Config.load_token()
    
    @staticmethod
    def get_hosts():
        return os.getenv('HOSTS', '')

    @staticmethod
    def get_db_pwd():
        return os.getenv('DB_PWD', '')

    @staticmethod
    def get_ca():
        return os.getenv('CA', '')
    
    @staticmethod
    def get_directory_id():
        return os.getenv('FOLDER_ID', '')

"""• Определяет класс Config для централизованного управления конфигурационными параметрами приложения.
• Загружает конфигурационные параметры из файла .env и из файла authorized_key.json.
• Предоставляет методы для получения значений конфигурационных параметров, а также для создания и получения JWT."""




"""# Получение токена Telegram-бота
telegram_bot_token = Config.get_telegram_bot_token()

# Получение API-ключа
api_key = Config.get_api_key()

# Получение JWT
iam_token = Config.get_iam_token()"""
