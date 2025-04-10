import sys
from io import BytesIO
from search import object_position
from distance import lonlat_distance
import requests
from PIL import Image


search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
location = input("Введите адрес: ")
start_point = object_position(location)[0:2]
address_ll = ",".join(start_point)

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    print("Ошибка выполнения запроса:")

# Преобразуем ответ в json-объект
json_response = response.json()

# Получаем первую найденную организацию.
organization = json_response["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]
work_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]

# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]
org_point = f"{point[0]},{point[1]}"
delta = "0.005"
apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "apikey": apikey,
    # добавим точки, чтобы указать найденную аптеку
    "pt": "{0},pm2dgl~{1},pm2wtl".format(org_point, address_ll)
}

dst = round(lonlat_distance(map(float, start_point), map(float, point)), 2)

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
print("Адрес аптеки:", org_address)
print("Название:", org_name)
print("Время работы:", work_time)
print("Расстояние:", dst, "м")

im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()