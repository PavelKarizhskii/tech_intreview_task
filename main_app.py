from loguru import logger

from dog_ceo_methods import DogCeoApiMethods
from yandex_disk_methods import YandexDiskMethods


class AppMethods:
    """Методы приложения для работы с изображениями собак и Яндекс-Диском"""

    def upload_dogs_images_to_disk(self, breed: str, path: str):
        """Функция загружает изображения указанной породы собак на Яндекс-Диск
        :param breed: название породы для загрузки изображений
        :param path: путь к папке на Яндекс-Диске
        """
        dog_api = DogCeoApiMethods()  # Создание экземпляра для работы с Dog CEO API
        yandex_disk = YandexDiskMethods()  # Создание экземпляра для работы с Яндекс-Диском

        # Проверяем наличие породы в справочнике
        if not dog_api.validate_breed(breed):
            logger.error(f"Порода {breed} отсутствует в справочнике")
            raise ValueError(f"Порода {breed} отсутствует в справочнике")

        # Получаем список URL-адресов изображений
        urls = dog_api.get_list_urls(breed)

        # Создаём папку на Яндекс.Диске
        yandex_disk.create_folder_disk(path)

        # Загрузка каждого изображения на Яндекс.Диск
        for url in urls:
            part_name = url.split('/')
            name = '_'.join([part_name[-2], part_name[-1]])  # Формируем имя файла на диске
            yandex_disk.upload_photos_to_disk(path, url, name)  # Загружаем фото на диск


if __name__ == "__main__":
    app = AppMethods()
    app.upload_dogs_images_to_disk(breed='dsfdsfsd', path="Неверная порода")
