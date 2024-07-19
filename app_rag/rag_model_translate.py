#Этот код реализует класс YandexTranslator, который предоставляет методы для перевода текста с помощью сервиса Яндекс.Перевод.

import requests #Импортируется модуль requests, который используется для отправки HTTP-запросов.

from langchain_core.documents.base import Document #Импортируется класс Document из библиотеки langchain_core, который представляет собой объект, содержащий текст документа и метаданные.

class YandexTranslator: #Определяет класс YandexTranslator, который предоставляет методы для перевода текста.

    def __init__(self, service_account_api_key) -> None: #Метод инициализации, принимает API-ключ для сервиса Яндекс.Перевод.
        self.service_api_key = service_account_api_key #Сохраняет API-ключ в атрибуте объекта.

    def translate_similar_docs_to_russian(self, docs): #Метод для перевода списка документов на русский язык.
        translated_docs = [] # Создается пустой список для хранения переведенных документов
        for doc in docs: #Проходит по списку документов.
            print(doc.page_content) #Выводит текст документа.
            translated_content = self._translate_text(doc.page_content, 'ru', 'zh') #Вызывает метод _translate_text для перевода текста документа с китайского (zh) на русский (ru).
            translated_content += f"\n\nСсылка на источник: {doc.metadata['url']}" # need to extract to dif func  #Добавляет ссылку на источник в конец переведенного текста.
            translated_docs.append(Document(page_content=translated_content, metadata=doc.metadata)) #Создает новый объект Document с переведенным текстом и метаданными, и добавляет его в список translated_docs.
        return translated_docs #Возвращает список переведенных документов.

    def translate_query_to_chinese(self, query): #Метод для перевода запроса на китайский язык.
        try: #Блок try...except обрабатывает возможные ошибки во время перевода.
            translated_query = self._translate_text(query, "zh", "ru")  #Вызывает метод _translate_text для перевода запроса с русского (ru) на китайский (zh).
            print("chinese: {translated_query}") # Выводит переведенный запрос.
            return translated_query #Возвращает переведенный запрос.
        except Exception as e: #Обрабатывает ошибки при переводе.
            print(f"An error occurred: {e}") #Выводит сообщение об ошибке.
            return None #Возвращает None, если произошла ошибка.
    
    def _translate_text(self, text, target_language, source_language) -> str: #Метод для перевода текста.
        url = "https://translate.api.cloud.yandex.net/translate/v2/translate" #Задает URL-адрес API Яндекс.Перевод.
        headers = { # Создает заголовки запроса, включающие API-ключ и тип контента
            "Authorization": f"Api-Key {self.service_api_key}",
            "Content-Type": "application/json",
        }
        body = { #Создает тело запроса, содержащее информацию о языке перевода, исходный текст и т.д
            "sourceLanguageCode": source_language,
            "targetLanguageCode": target_language,
            "texts": [text],
        }
        response = requests.post(url, headers=headers, json=body, timeout=300) # Отправляет POST-запрос к API Яндекс.Перевод.
        result = response.json() #Преобразует ответ API в JSON-объект.
        print(result) #Выводит результат перевода.

        if "translations" in result: #Проверяет, есть ли в результате перевод.
            return result["translations"][0]["text"]  #Возвращает переведенный текст.
        else: #Если перевода нет, выбрасывает исключение.
            raise Exception(f"Error in translation: {result}") #Выбрасывает исключение, сообщая об ошибке при переводе.


"""• Реализует класс YandexTranslator для использования API Яндекс.Перевод.
• Предоставляет методы для перевода текста, документов и запросов.
• Обрабатывает возможные ошибки при переводе.

Пример использования:

# Инициализация YandexTranslator
translator = YandexTranslator()
translator.init('YOUR_API_KEY')

# Перевод текста
translated_text = translator.translate_text('Привет, мир!', 'ru', 'en')
print(translated_text)

# Перевод документа
doc = Document(page_content='Текст документа на китайском языке', metadata={'url': 'https://example.com'})
translated_doc = translator.translate_similar_docs_to_russian([doc])
print(translated_doc)

# Перевод запроса
translated_query = translator.translate_query_to_chinese('Какой сегодня день?')
print(translated_query) """
