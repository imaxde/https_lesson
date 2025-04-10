import requests

query = input("Введите адрес: ")
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
apikey = "8013b162-6b42-4997-9691-77b7074026e0"

geocoder_params = {"apikey": apikey, "geocode": query, "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
location = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]
coordinates = location["GeoObject"]["Point"]["pos"].replace(" ", ",")

geocoder_params = {"apikey": apikey, "geocode": coordinates, "format": "json", "kind": "district"}
response = requests.get(geocoder_api_server, params=geocoder_params)
location = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]
district = location["GeoObject"]["name"]

print(district)