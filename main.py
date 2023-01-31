import sys
from io import BytesIO
import requests
from PIL import Image
from make_spn import spn_value
from distance import lonlat_distance

toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address_ll = ",".join([toponym_longitude, toponym_lattitude])

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
json_2 = response.json()
toponym = json_2["features"][0]
coords = json_2["features"][0]["geometry"]["coordinates"]
pharmacy_coordinates = f"{coords[0]},{coords[1]}"
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": spn_value(str(toponym_longitude), str(coords[0])),
    "l": "map",
    "pt": ",".join([toponym_longitude, toponym_lattitude, "home~" + pharmacy_coordinates, "flag"])
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
distance = int(lonlat_distance(toponym_coodrinates.split(), coords))
adress = toponym["properties"]["CompanyMetaData"]["address"]
name = toponym["properties"]["CompanyMetaData"]["name"]
time = toponym["properties"]["CompanyMetaData"]["Hours"]["text"]
print(f'Расстояние до аптеки: {distance}м.')
print(f"Название аптеки: {name}")
print(f"Адресс аптеки: {adress}")
print(f"Время работы: {time}")