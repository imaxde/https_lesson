import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт
from search import object_position
import requests
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python polniy-poisk.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

t = object_position(toponym_to_find)
apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([t[0], t[1]]),
    "spn": ",".join([t[2], t[3]]),
    "apikey": apikey,
    "pt": f"{t[0]},{t[1]},org"
}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.save("img.png")
opened_image.show()  # Создадим картинку и тут же ее покажем встроенным просмотрщиком операционной системы

