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

json_response = response.json()

organizations = json_response["features"]
pts = []
for i in organizations:
    work_time = i["properties"]["CompanyMetaData"]["Hours"]
    point = i["geometry"]["coordinates"]
    if "TwentyFourHours" in work_time["Availabilities"][0]:
        style = "pmgnm"
    elif "Intervals" in work_time["Availabilities"][0]:
        style = "pmblm"
    else:
        style = "pmgrm"
    pts.append(f"{point[0]},{point[1]},{style}")

apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

map_params = {
    "apikey": apikey,
    # добавим точки, чтобы указать найденную аптеку
    "pt": "~".join(pts)
}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()