""" Этот код реализует класс OpenSearchDB, который предоставляет методы для работы
с OpenSearch, инструментом поиска, для поиска схожих документов. Давайте разберем его по строкам: """

from opensearchpy import OpenSearch

from langchain.vectorstores import OpenSearchVectorSearch #Импортируется класс OpenSearchVectorSearch из библиотеки langchain, который используется для поиска векторных представлений документов в OpenSearch.
from langchain_huggingface import HuggingFaceEmbeddings #Импортируется класс HuggingFaceEmbeddings из библиотеки langchain_huggingface, который позволяет использовать модели встраивания (embeddings) из Hugging Face.

embedding_model_name = "DMetaSoul/sbert-chinese-general-v2"

"""Задается имя модели встраивания, которая будет использоваться для преобразования текстов в векторные представления.
В данном случае, это модель sbert-chinese-general-v2 от DMetaSoul."""

embeddings_model = HuggingFaceEmbeddings(
    model_name=embedding_model_name, model_kwargs={"device": "cpu"} """ Создается объект HuggingFaceEmbeddings, используя заданное
    имя модели и model_kwargs={"device": "cpu"}, чтобы указать, что модель должна работать на процессоре (CPU)."""
)

class OpenSearchDB: """Определяет класс OpenSearchDB, который предоставляет методы для работы с OpenSearch."""

    def __init__(self, ca: str, pwd: str, hosts: str) -> None: """Метод инициализации, принимает сертификат (ca), пароль (pwd) и адрес OpenSearch (hosts)."""
        self._init_connection(ca=ca, pwd=pwd, hosts=hosts) """Вызывает метод _init_connection для инициализации подключения к OpenSearch."""

    def _init_connection(self, ca, pwd, hosts): """Метод инициализации подключения к OpenSearch."""
        print(hosts, pwd)  """Выводит адрес OpenSearch и пароль. """
        self.docsearch : OpenSearchVectorSearch = OpenSearchVectorSearch( """Создается объект OpenSearchVectorSearch, который будет использоваться для поиска в OpenSearch."""
            embedding_function=embeddings_model, """ Указывает модель встраивания, которая будет использоваться для конвертации текстов в векторы."""
            index_name="china-embeddings", """Указывает имя индекса в OpenSearch, где хранятся векторы документов."""
            opensearch_url=hosts, """ Указывает адрес OpenSearch."""
            http_auth=("admin", pwd), """Указывает аутентификацию пользователя "admin" с паролем pwd."""
            use_ssl=True, #Настраивает использование SSL-соединения с проверкой сертификатов и сертификатом ca.
            verify_certs=True, #Устанавливает таймаут для запросов к OpenSearch на 300 секунд.
            ca_certs=ca,
            timeout=300
        )

    def find_similar(self, translated_query, year=2023): #Метод для поиска похожих документов.
        pre_filter_dict = {"range": {"metadata.year": {"lte": year}}} #Создает словарь фильтрации, который будет использоваться для поиска документов не старше указанного year.
        documents = self.docsearch.max_marginal_relevance_search(translated_query) """Выполняет поиск похожих документов в OpenSearch с использованием запроса translated_query и алгоритма max_marginal_relevance_search для поиска релевантных документов."""
        return documents #Возвращает список найденных документов.

"""• Создает класс OpenSearchDB, который инициализирует подключение к OpenSearch.
• Использует модель встраивания для конвертации текстов в векторы.
• Предоставляет метод find_similar для поиска похожих документов в OpenSearch.

Пример использования:"""

"""# Инициализация OpenSearchDB
opensearch_db = OpenSearchDB()
opensearch_db.init(ca='YOUR_CA_CERT', pwd='YOUR_PASSWORD', hosts='YOUR_OPENSEARCH_URL')

# Запрос
translated_query = 'Текст запроса на китайском языке'

# Поиск похожих документов
documents = opensearch_db.find_similar(translated_query)

# Вывод результата
print(documents)"""

