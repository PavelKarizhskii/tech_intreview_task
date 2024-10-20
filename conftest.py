import pytest
from loguru import logger

from dog_ceo_methods import DogCeoApiMethods
from yandex_disk_methods import YandexDiskMethods

PATH_TO_TEST_FOLDER = "test_folder"


@pytest.fixture()
def get_breed_without_sub_breeds() -> str:
    """Возвращает название породы без подвидов"""
    logger.info(f"Запрос породы без под-пород")
    dog_api = DogCeoApiMethods()
    breeds = dog_api.get_list_all_breeds().json().get('message', {})
    for breed, sub_breeds in breeds.items():
        if not sub_breeds:
            return breed


@pytest.fixture()
def get_breed_with_some_sub_breeds() -> str:
    """Возвращает название породы с более чем двумя подвидами"""
    logger.info(f"Запрос породы с тремя и более под-пород")
    dog_api = DogCeoApiMethods()
    breeds = dog_api.get_list_all_breeds().json().get('message', {})
    for breed, sub_breeds in breeds.items():
        if len(sub_breeds) > 2:
            return breed


@pytest.fixture()
def delete_test_folder():
    """Пытается удалить тестовую папку при старте тестов(если папка по какой-то из причин не была удалена).
    Удаляет тестовую папку после прогона тестов.
    """
    logger.info(f"Подготовка тестовой папки")
    yandex_disk = YandexDiskMethods()
    path = PATH_TO_TEST_FOLDER
    yandex_disk.delete_resource(path=path)
    yield
    yandex_disk.delete_resource(path=path)
