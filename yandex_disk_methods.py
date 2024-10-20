import time
from loguru import logger
import os
import allure

from dog_ceo_methods import DogCeoApiMethods
from api_client import ApiClient


class YandexDiskMethods:
    """Методы для работы с Яндекс-Диском: создание новых папок, загрузка файлов"""

    # Базовый URL для работы с ресурсами Яндекс Диска
    BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources'
    TRASH_URL = 'https://cloud-api.yandex.net/v1/disk/trash/resources'

    def __init__(self):
        """Инициализация с передачей токена. Если токен не передан, он будет загружен из переменной окружения."""
        self.token = os.getenv('YANDEX_DISK_TOKEN')
        self.api_client = ApiClient()
        self.dog_ceo_methods = DogCeoApiMethods()
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    @allure.step("Создание папки на диске по пути: {path}")
    def create_folder_disk(self, path: str):
        """Создает пустую папку в корневом каталоге диска.
        :param path: Путь для создания папки
        """
        logger.info(f"Создание папки на диске по пути: {path}")
        response = self.api_client.put(url=f'{self.BASE_URL}?path={path}', headers=self.headers)
        return response

    @allure.step("Загрузка фото с именем {name} по URL {url_file} на диск по пути {path}")
    def upload_photos_to_disk(self, path: str, url_file: str, name: str):
        """Загружает фото по ссылке на диск.
        :param path: Путь на диске для загрузки
        :param url_file: ссылка на файл для загрузки
        :param name: имя файла на диске
        """
        logger.info(f"Загрузка фото с именем {name} c {url_file} на диск по пути {path}")
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {"path": f'/{path}/{name}', 'url': url_file, "overwrite": "true"}
        response = self.api_client.post(url=upload_url, headers=self.headers, params=params)
        return response

    @allure.step("Получение информации о ресурсе на диске по пути: {path}")
    def get_information_resource_on_disk(self, path: str):
        """Запрашивает метаинформацию о ресурсе (свойства файла или папки, содержимое папки).
        :param path: Путь на диске
        """
        logger.info(f"Получение информации о папке на диске по пути: {path}")
        response = self.api_client.get(url=f'{self.BASE_URL}?path=/{path}', headers=self.headers)
        return response

    @allure.step("Удаление ресурса на диске по пути: {path} и очистка корзины")
    def delete_resource(self, path: str):
        """Удаляет папку с диска и очищает корзину.
        :param path: Путь на диске
        """
        logger.info(f"Удаление папки с диска по пути: {path} и очистка корзины")
        self.api_client.delete(url=f'{self.BASE_URL}?path=/{path}', headers=self.headers)
        time.sleep(10)
        response = self.api_client.delete(url=self.TRASH_URL, headers=self.headers)
        return response

    @allure.step("Проверка создания папки на диске по пути: {path}")
    def check_create_folder(self, path: str) -> bool:
        """Проверяет создание папки на диске.
        :param path: Путь на диске
        """
        logger.info(f"Проверка наличия папки с именем: {path} на диске")
        retry_count = 3
        for _ in range(retry_count):
            response = self.get_information_resource_on_disk(path)
            if response.json()['type'] == "dir" and response.json()['name'] == path:
                return True
            else:
                time.sleep(0.5)
        return False

    @allure.step("Проверка количества изображений породы {breed} в папке по пути: {path}")
    def check_number_images_in_folder(self, path: str, breed: str) -> bool:
        """Проверяет количество изображений указанной пароды на диске
        :param breed: порода собаки, для которой загружаются изображения
        :param path: путь на диске
        """
        logger.info(f"Проверка наличия папки на диске по пути: {path} с изображениями пароды {breed}")
        retry_count = 3
        list_sub_breeds = self.dog_ceo_methods.get_list_sub_breeds(breed).json().get('message', [])

        for _ in range(retry_count):
            try:
                response = self.get_information_resource_on_disk(path)
                if list_sub_breeds:
                    assert len(response.json()['_embedded']['items']) == len(list_sub_breeds), \
                        "Проверяем, что в кол-во файлов в папке соответствует кол-ву под-парод"
                    for item in response.json()['_embedded']['items']:
                        # Проверяем, что в папке только файлы название которых начинается с названия выбранной пароды
                        assert item['type'] == 'file'
                        assert item['name'].startswith(breed)
                    return True
                else:
                    assert len(response.json()['_embedded']['items']) == 1, \
                        "Проверяем, что в кол-во файлов в папке соответствует кол-ву под-парод"
                    for item in response.json()['_embedded']['items']:
                        # Проверяем, что в папке только файлы название которых начинается с названия выбранной пароды
                        assert item['type'] == 'file'
                        assert item['name'].startswith(breed)
                    return True
            except (AssertionError, KeyError):
                time.sleep(5)
        return False


if __name__ == "__main__":
    disk = YandexDiskMethods()
    disk.create_folder_disk("NEW_FOLDER")
    disk.get_information_resource_on_disk("NEW_FOLDER")
    print(disk.check_create_folder("NEW_FOLDER"))
    disk.delete_resource("NEW_FOLDER")
