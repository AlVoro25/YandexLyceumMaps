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
toponym = json_2["features"]
pharmaces = toponym[:10]
points = [f"{pharmacy['geometry']['coordinates'][0]},{pharmacy['geometry']['coordinates'][1]}" for pharmacy in pharmaces]
maxi = 0
point2 = 0
lat = False
for pharmacy in pharmaces:
    if "Hours" in pharmacy["properties"]["CompanyMetaData"].keys():
        if "круглосуточно" in pharmacy["properties"]["CompanyMetaData"]["Hours"]["text"]:
            points[pharmaces.index(pharmacy)] += ",pmgns"
        else:
            points[pharmaces.index(pharmacy)] += ",pmdbs"
    else:
        points[pharmaces.index(pharmacy)] += ",pmgrs"
    if abs(float(pharmacy["geometry"]["coordinates"][0]) - float(toponym_longitude)) > maxi:
        maxi = abs(float(pharmacy["geometry"]["coordinates"][0]) - float(toponym_longitude))
        point2 = float(pharmacy["geometry"]["coordinates"][0])
        lat = False
    if abs(float(pharmacy["geometry"]["coordinates"][1]) - float(toponym_lattitude)) > maxi:
        maxi = abs(float(pharmacy["geometry"]["coordinates"][1]) - float(toponym_lattitude))
        point2 = float(pharmacy["geometry"]["coordinates"][1])
        lat = True
points = "~".join(points)
coords = json_2["features"][0]["geometry"]["coordinates"]
pharmacy_coordinates = f"{coords[0]},{coords[1]}"
if not lat:
    to_check = toponym_longitude
else:
    to_check = toponym_lattitude
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": spn_value(str(to_check), str(point2)),
    "l": "map",
    "pt": points
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()