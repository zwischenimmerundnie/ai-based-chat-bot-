"""Этот код реализует класс YandexLLM, который позволяет взаимодействовать с YandexGPT 
(языковой моделью от Yandex) через библиотеку LangChain для обработки текста и ответов на вопросы. Давайте разберем его по строкам:"""


import langchain
from langchain.chains import LLMChain #Класс для создания цепочки с языковой моделью.
from langchain_community.llms import YandexGPT #Класс для использования YandexGPT.
from langchain_core.documents.base import Document # Класс для представления документа.
from langchain.chains.combine_documents.stuff import StuffDocumentsChain #Класс для создания цепочки, которая "вставляет" весь контекст в prompt.
from langchain_core.prompts import PromptTemplate #Класс для создания шаблонов prompts.
from langchain_core.runnables import RunnableSequence #Класс для создания последовательности задач.

stuff_prompt_override = """
Ты - ассистент востоковеда. Ты умеешь читать новости на китайском языке, анализировать их, находить нужную информацию и переводить ее на русский. Ты отвечаешь на вопросы о Китае. Ответы ты находишь в тексте новостей. 

Для имен собственных ты дополнительно приводишь оригинальное написание на китайском (приводишь цитату из источника). Для объектов в новости ты приводишь обобщающую характеристику. Например, если в ответе перечисляются автомобильные компании, то помимо их названия указывается юридическая принадлежность, время создания, специализация (авто для широкого покупателя, авто премиум класса, электромобили, строительные машины и т.п.), оценка размера (считается крупной, ведущей, прошлогодний стартап и т.п.), отношение к другим компаниям (подразделение, дочерняя компания, подрядчик крупного концерна и т.п.). Если по одному и тому же запросу ты находишь разные сведения, прикрепляй каждую точку зрения и указывай ссылку на источник.

Ответы должны быть четко структурированы и включать следующие элементы:
1. Описание события или факта.
2. Подробная информация об участвующих лицах или объектах.
3. Оригинальные имена собственных на китайском языке с цитатой из источника (по возможности).
4. К каждому тезису приводи URL ссылку на статью источник.
---
Текст:
-----
{context}
-----
Вопрос:
{query}
"""

""" Это строка, представляющая собой prompt, который будет использоваться для языковой модели. 
  * В prompte заданы роли, ожидания, формат ответа и требования к использованию источников.
  * В prompte используются переменные {context} и {query}, которые будут заменены на текст и вопрос соответственно.
  """
class YandexLLM: #Определяет класс YandexLLM, который инициализирует и управляет взаимодействием с YandexGPT.

    def __init__(self, api_key, folder_id, iam_token = '') -> None: #Инициализирует объект YandexLLM.
        self.llm = YandexGPT( #Создает объект YandexGPT, используя api_key и folder_id для аутентификации с YandexGPT.
            api_key=api_key, #Создает объект YandexGPT, используя api_key и folder_id для аутентификации с YandexGPT.
            folder_id=folder_id) #Создает объект YandexGPT, используя api_key и folder_id для аутентификации с YandexGPT.
        self._init_chain() #ызывает метод для создания цепочки для обработки текста.

    def _init_chain(self): #Создает цепочку StuffDocumentsChain для обработки текста и ответов на вопросы:

        # Промпт для обработки документов
        document_prompt = PromptTemplate( #Создает prompt для обработки текста документов, используя шаблон {page_content}.
            input_variables=["page_content"], template="{page_content}"
        )

        # Промпт для языковой модели
        document_variable_name = "context"
        prompt = PromptTemplate( #Создает prompt для YandexGPT, используя шаблон stuff_prompt_override и переменные {context} и {query}
            template=stuff_prompt_override, input_variables=["context", "query"]
        )

        # Создаём цепочку
        llm_chain = LLMChain(llm=self.llm, prompt=prompt) #Создает цепочку LLMChain, используя объект self.llm и prompt для YandexGPT.
        self.chain = StuffDocumentsChain(
            llm_chain=llm_chain, #Создает цепочку StuffDocumentsChain, которая объединяет текст документов, используя document_prompt, и использует llm_chain для получения ответа.
            document_prompt=document_prompt,
            document_variable_name=document_variable_name,
        )

    def invoke_chain(self, input_context : list[Document], query : str): #Метод для вызова цепочки обработки текста.
        if input_context: #Проверяет, есть ли входящие документы.
            # Adjust your code to include an 'input' dictionary
            input_data = { #Создает словарь input_data, содержащий входящие документы (input_documents) и запрос (query).
                'input_documents': input_context,
                'query': query,  # Используем оригинальный русский запрос
            }
            # Now, pass the 'input_data' dictionary to the 'invoke' method
            response = self.chain.invoke(input=input_data) #Вызывает цепочку self.chain с данными input_data и получает ответ
            return response['output_text'] #Возвращает текст ответа из response.
        else:
"""• Определяет класс YandexLLM, который предоставляет интерфейс для работы с YandexGPT через LangChain.
• Создает цепочку StuffDocumentsChain для обработки текста и ответов на вопросы.
• Выполняет цепочку, используя входящие документы и запрос, и возвращает текст ответа.
"""

"""пример использования

# Инициализация YandexLLM
yandex_llm = YandexLLM()
yandex_llm.init(api_key='YOUR_API_KEY', folder_id='YOUR_FOLDER_ID')

# Документы, содержащие текст
documents = [Document(page_content='Текст документа 1'), Document(page_content='Текст документа 2')]

# Запрос
query = 'Какой сегодня день?'

# Вызов цепочки обработки текста
response = yandex_llm.invoke_chain(documents, query)

# Вывод ответа
print(response)

"""
            print("No relevant documents found.") #Если входящих документов нет, выводит сообщение "No relevant documents found.".
