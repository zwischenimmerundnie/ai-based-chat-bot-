"""Этот код реализует класс BotPresenter, который отвечает за обработку запросов пользователя и взаимодействие
с различными компонентами приложения: переводчиком, языковой моделью и базой данных. Давайте разберем его по строкам:"""

from app_rag.rag_model_translate import YandexTranslator #Импортируется класс YandexTranslator из модуля app_rag.rag_model_translate.
from app_rag.rag_model_gpt import YandexLLM #Импортируется класс YandexLLM из модуля app_rag.rag_model_gpt.
from app_rag.rag_model_opensearch import OpenSearchDB #Импортируется класс OpenSearchDB из модуля app_rag.rag_model_opensearch.

class BotPresenter: #Определяет класс BotPresenter.

    def __init__(self, translator : YandexTranslator, llm : YandexLLM, database : OpenSearchDB) -> None: # Метод инициализации, принимает в качестве аргументов объекты переводчика, языковой модели и базы данных.
        self.translator = translator #Сохраняет объект YandexTranslator в атрибуте self.translator.
        self.period = 2023 #Задает период для поиска документов, устанавливая  значение 2023.
        self.llm = llm  # Сохраняет объект YandexLLM в атрибуте self.llm.
        self.database = database #Сохраняет объект OpenSearchDB в атрибуте self.database.
    
    def send_query(self, query): #Метод для обработки запроса пользователя.
        zh_version = self.translator.translate_query_to_chinese(query) #Переводит запрос на китайский язык, используя метод translate_query_to_chinese объекта self.translator.
        print(zh_version) 
        similar_documents = self.database.find_similar(zh_version, self.period) #Ищет похожие документы в базе данных self.database, используя переведенный запрос и период self.period.
        print(similar_documents) 
        ru_docs_versions = self.translator.translate_similar_docs_to_russian(similar_documents) #Переводит найденные документы на русский язык, используя метод 
        response = self.llm.invoke_chain(similar_documents, ru_docs_versions) #Передает найденные документы и их переводы в языковую модель self.llm для получения ответа.
        return response # Возвращает ответ от языковой модели.

