import pytest

from yandex_disk_methods import YandexDiskMethods
from main_app import AppMethods
from conftest import PATH_TO_TEST_FOLDER


def test_check_upload_dog_without_sub_breeds(get_breed_without_sub_breeds, delete_test_folder):
    """Проверка загрузки изображения пароды без под-парод"""
    yandex_disk = YandexDiskMethods()
    app_methods = AppMethods()

    # Получаем породу без подвидов
    breed = get_breed_without_sub_breeds

    # Загрузка изображений на Яндекс.Диск
    app_methods.upload_dogs_images_to_disk(breed, path=PATH_TO_TEST_FOLDER)

    # Проверка, что папка была создана
    assert yandex_disk.check_create_folder(PATH_TO_TEST_FOLDER), "Папка для файлов не была создана."

    # Проверка, что изображения были загружены
    assert yandex_disk.check_number_images_in_folder(PATH_TO_TEST_FOLDER, breed), "Изображения не были загружены."


def test_check_upload_dog_with_some_sub_breeds(get_breed_with_some_sub_breeds, delete_test_folder):
    """Проверка загрузки изображения пароды с несколькими под-породами"""
    yandex_disk = YandexDiskMethods()
    app_methods = AppMethods()

    # Получаем породу с более чем двумя подвидами
    breed = get_breed_with_some_sub_breeds

    # Загрузка изображений на Яндекс.Диск
    app_methods.upload_dogs_images_to_disk(breed, path=PATH_TO_TEST_FOLDER)

    # Проверка, что папка была создана
    assert yandex_disk.check_create_folder(PATH_TO_TEST_FOLDER), "Папка для файлов не была создана."

    # Проверка, что изображения были загружены
    assert yandex_disk.check_number_images_in_folder(PATH_TO_TEST_FOLDER, breed), "Изображения не были загружены."


def test_upload_dog_with_incorrect_breed(delete_test_folder):
    """Проверка обработки некорректной породы собаки"""
    app_methods = AppMethods()

    # Попытка загрузки изображений несуществующей породы
    with pytest.raises(ValueError) as exc_info:
        app_methods.upload_dogs_images_to_disk("non_existent_breed", path=PATH_TO_TEST_FOLDER)

    # Проверка, что было вызвано исключение с правильным сообщением
    assert str(exc_info.value) == "Порода non_existent_breed отсутствует в справочнике"
