from loguru import logger
import allure

from api_client import ApiClient
from pydantic_models_dog_ceo import GetListSubBreedsResponse


class DogCeoApiMethods:
    """Класс для работы с API https://dog.ceo/"""

    # Базовый URL для работы с Dog CEO API
    dog_base_url = "https://dog.ceo/api/"

    def __init__(self):
        """Инициализация с созданием экземпляра ApiClient"""
        self.api_client = ApiClient()

    @allure.step("Запрос под-пород для породы {breed}")
    def get_list_sub_breeds(self, breed: str):
        """Запрос под-пород породы
        :param breed: название породы, для которой требуется найти под-породу
        """
        logger.info(f"Запрос подвидов для породы: {breed}")
        response = self.api_client.get(url=f'{self.dog_base_url}breed/{breed}/list')
        # Валидация схемы JSON
        if response.status_code == 200:
            GetListSubBreedsResponse(**response.json())
        return response

    @allure.step("Запрос списка всех пород")
    def get_list_all_breeds(self):
        """Запрос всех пород"""
        logger.info("Запрос списка всех пород")
        response = self.api_client.get(url=f'{self.dog_base_url}breeds/list/all')
        return response

    @allure.step("Проверка наличия пароды в справочнике")
    def validate_breed(self, breed: str) -> bool:
        """
        Проверка наличия пароды в справочнике dog.ceo

        :param breed: название породы для проверки
        :return: True, если порода существует, False в противном случае
        """
        logger.info("Проверка наличия пароды в справочнике")
        all_breeds = self.get_list_all_breeds().json().get('message', {})
        return breed in all_breeds

    @allure.step("Запрос изображения для породы {breed} и под-породы {sub_breed}")
    def get_image_urls(self, breed: str, sub_breed: str = ""):
        """Запрос изображения пса по указанной породе и под-породе
        :param breed: название породы
        :param sub_breed: под-порода
        """
        logger.info(f"Запрос изображения под-породы: {sub_breed} породы: {breed}")
        if sub_breed:
            response = self.api_client.get(url=f"{self.dog_base_url}breed/{breed}/{sub_breed}/images/random")
        else:
            response = self.api_client.get(url=f"{self.dog_base_url}breed/{breed}/images/random")
        return response

    @allure.step("Получение списка ссылок на изображения породы {breed}")
    def get_list_urls(self, breed: str) -> list:
        """Возвращает список ссылок на изображения собак
        :param breed: название породы, для которой выполняется поиск изображений
        """
        logger.info(f"Получение списка ссылок на изображения породы: {breed}")
        url_images = []
        sub_breeds = self.get_list_sub_breeds(breed).json().get('message')
        if sub_breeds:
            for sub_breed in sub_breeds:
                response = self.get_image_urls(breed=breed, sub_breed=sub_breed)
                sub_breed_urls = response.json().get('message')
                url_images.append(sub_breed_urls)
        else:
            url_images.append(self.get_image_urls(breed=breed).json().get('message'))
        return url_images


if __name__ == "__main__":
    dog = DogCeoApiMethods()
    dog.get_list_all_breeds()
    print(dog.get_list_urls('bakharwal'))
