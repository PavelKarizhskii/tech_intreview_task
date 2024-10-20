import sys

from loguru import logger
import requests
import allure

# Настройка логирования через loguru. В полноценном проекте настройки будут вынесены в отдельный файл
# Также при необходимости можно реализовать запись логов в файл
logger.remove()
logger.add(sink=sys.stdout, level="INFO", format="<green>{time}</green> - <magenta>{level}</magenta> - {message}",
           colorize=True)

HEADERS = {'Content-Type': 'application/json; charset=utf-8'}


class ApiClient:
    """Реализация методов апи для упрощения настройки логирования и отчетов"""
    def __init__(self):
        pass

    @allure.step("GET запрос к {url}")
    def get(self, url, params: dict = None, headers: dict = None, cookies: dict = None):
        if headers is None:
            headers = HEADERS
        logger.info(f"Отправляем GET запрос к {url} с параметрами: {params} и headers: {headers} и cookies: {cookies}")
        response = requests.get(url, params=params, headers=headers)
        self.log_response(response)
        return response

    @allure.step("POST запрос к {url}")
    def post(self, url, json_body: dict = None, headers: dict = None, cookies: dict = None, params: dict = None):
        if headers is None:
            headers = HEADERS
        logger.info(f"Отправляем POST запрос к {url} с JSON: {json_body} headers: {headers} и cookies: {cookies} и "
                    f"{params}")
        response = requests.post(url, json=json_body, headers=headers, cookies=cookies, params=params)
        self.log_response(response)
        return response

    @allure.step("PUT запрос к {url}")
    def put(self, url, json_body: dict = None, headers: dict = None, cookies: dict = None, params: dict = None):
        if headers is None:
            headers = HEADERS
        logger.info(f"Отправляем PUT запрос к {url} с JSON: {json_body} headers: {headers} и cookies: {cookies} и "
                    f"{params}")
        response = requests.put(url, json=json_body, headers=headers, cookies=cookies, params=params)
        self.log_response(response)
        return response

    @allure.step("DELETE запрос к {url}")
    def delete(self, url, params=None, headers=None, cookies: dict = None):
        if headers is None:
            headers = HEADERS
        logger.info(f"Отправляем DELETE запрос к {url} с параметрами: {params} headers: {headers} и cookies: {cookies}")
        response = requests.delete(url, headers=headers, params=params, cookies=cookies)
        self.log_response(response)
        return response

    @allure.step("Логирование ответа")
    def log_response(self, response):
        logger.info(f"Статус код: {response.status_code}")
        logger.info(f"Тело ответа: {response.text}\n")
        allure.attach(
            body=response.text,
            name="Ответ API",
            attachment_type=allure.attachment_type.JSON if response.headers.get('Content-Type') == 'application/json'
            else allure.attachment_type.TEXT
        )
