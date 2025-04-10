import requests


def object_position(geocode):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": geocode,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        return
        # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    # Верхний левый угол
    upper_corner = toponym["boundedBy"]["Envelope"]["upperCorner"].split()
    # Нижний правый угол
    lower_corner = toponym["boundedBy"]["Envelope"]["lowerCorner"].split()
    # Дельта
    delta_y = round(abs(float(upper_corner[0]) - float(lower_corner[0])), 7)
    delta_x = round(abs(float(upper_corner[1]) - float(lower_corner[1])), 7)
    return toponym_longitude, toponym_lattitude, str(delta_y), str(delta_x)






