from math import asin, cos, radians, sin, sqrt
from typing import Dict, List

import geopy.distance
import requests
from geojson import Feature, Point, Polygon
from turfpy.measurement import boolean_point_in_polygon

URL: str = 'https://geocode-maps.yandex.ru/1.x/'
mkad_points: List = [
  [55.774543, 37.842663],
  [55.774543, 37.842663],
  [55.765129, 37.84269],
  [55.75589, 37.84216],
  [55.747672, 37.842232],
  [55.739098, 37.841109],
  [55.730517, 37.840112],
  [55.721782, 37.839555],
  [55.712173, 37.836968],
  [55.702566, 37.832449],
  [55.694271, 37.829557],
  [55.685214, 37.831425],
  [55.676732, 37.834695],
  [55.66763, 37.837543],
  [55.658535, 37.839295],
  [55.650881, 37.834713],
  [55.643749, 37.824948],
  [55.636433, 37.813746],
  [55.629521, 37.803083],
  [55.623666, 37.793022],
  [55.617657, 37.781614],
  [55.61114, 37.769945],
  [55.604819, 37.758428],
  [55.599077, 37.747199],
  [55.594763, 37.736949],
  [55.588135, 37.721013],
  [55.58407, 37.709416],
  [55.578971, 37.695708],
  [55.574157, 37.682709],
  [55.57209, 37.668471],
  [55.572767, 37.649948],
  [55.573749, 37.63252],
  [55.574579, 37.619243],
  [55.575648, 37.600828],
  [55.577785, 37.586814],
  [55.581383, 37.571866],
  [55.584782, 37.55761],
  [55.590027, 37.534541],
  [55.59166, 37.527732],
  [55.596173, 37.512227],
  [55.602902, 37.501959],
  [55.609685, 37.493874],
  [55.616259, 37.485682],
  [55.623066, 37.477812],
  [55.63252, 37.466709],
  [55.639568, 37.459074],
  [55.646802, 37.450135],
  [55.65434, 37.441691],
  [55.66177, 37.433292],
  [55.671509, 37.425513],
  [55.680179, 37.418497],
  [55.687995, 37.414338],
  [55.695418, 37.408076],
  [55.70247, 37.397934],
  [55.709784, 37.388978],
  [55.718354, 37.38322],
  [55.725427, 37.379681],
  [55.734978, 37.37483],
  [55.745291, 37.370131],
  [55.754978, 37.369368],
  [55.763022, 37.369062],
  [55.771408, 37.369691],
  [55.782309, 37.370086],
  [55.789537, 37.372979],
  [55.796031, 37.37862],
  [55.806252, 37.387047],
  [55.81471, 37.390523],
  [55.824147, 37.393371],
  [55.832257, 37.395176],
  [55.840831, 37.394476],
  [55.850767, 37.392949],
  [55.858756, 37.397368],
  [55.866238, 37.404564],
  [55.872996, 37.417446],
  [55.876839, 37.429672],
  [55.88101, 37.443129],
  [55.882904, 37.45955],
  [55.88513, 37.474237],
  [55.889361, 37.489634],
  [55.894737, 37.503001],
  [55.901823, 37.519072],
  [55.905654, 37.529367],
  [55.907682, 37.543749],
  [55.909418, 37.559757],
  [55.910881, 37.575423],
  [55.90913, 37.590488],
  [55.904902, 37.607035],
  [55.901152, 37.621911],
  [55.898735, 37.633014],
  [55.896458, 37.652993],
  [55.895661, 37.664905],
  [55.895106, 37.681443],
  [55.894046, 37.697513],
  [55.889997, 37.711276],
  [55.883636, 37.723681],
  [55.877359, 37.736168],
  [55.872743, 37.74437],
  [55.866137, 37.75718],
  [55.8577, 37.773646],
  [55.854234, 37.780284],
  [55.848038, 37.792322],
  [55.840007, 37.807961],
  [55.835816, 37.816127],
  [55.828718, 37.829665],
  [55.821325, 37.836914],
  [55.811538, 37.83942],
  [55.802472, 37.840166],
  [55.793925, 37.841145]
]  # Каждый километр МКАД


def get_lat_and_long(needed_address: str) -> List:
    """Получает на вход строчный адрес, выдает координаты."""
    params: Dict[str, str] = {
        'apikey': '79d964e1-e572-4286-89c3-cc68fab189fc',
        'format': 'json',
        'geocode': needed_address
    }
    address: requests.models.Response = requests.get(URL, params=params)
    latitude: float = float((
      address.json()['response']['GeoObjectCollection']['featureMember'][0]
      ['GeoObject']['Point']['pos'][10:20]))  # Вычисление широты
    longitude: float = float((
      address.json()['response']['GeoObjectCollection']['featureMember'][0]
      ['GeoObject']['Point']['pos'][0:9]))  # Вычисление долготы
    return [latitude, longitude]


def is_in_mkad(needed_address: List) -> bool:
    """Проверяет находится ли адрес внутри МКАД"""
    point: List = Feature(geometry=Point(needed_address))  # Нахождение точки
    polygon: List = Polygon([mkad_points])  # Создание полигона
    statement = boolean_point_in_polygon(point, polygon)
    # Проверка на совпадение
    return statement


def dist_between_two_lat_lon(*args) -> float:
    """Математическое нахождение дистанции между двумя точками"""
    lat1, lat2, long1, long2 = map(radians, args)

    dist_lats: float = abs(lat2 - lat1)
    dist_longs: float = abs(long2 - long1)
    a: float = sin(dist_lats / 2) ** 2 + cos(lat1) * cos(lat2) * sin(
        dist_longs / 2) ** 2
    c: float = asin(sqrt(a)) * 2
    radius_earth: int = 6378
    return c * radius_earth


def find_closest_lat_lon(address: List) -> List:
    """Находит ближайшую точку МКАД к нужному адресу"""
    return min(mkad_points, key=lambda p: dist_between_two_lat_lon(
                    address[0], address[1], p[0], p[1]))


def get_distance(needed_address: List, nearest_mkad_point: List) -> float:
    """Считает дистанцию между ближайшей точкой на МКАД и нужным адресом"""
    distance: float = geopy.distance.geodesic(
        needed_address, nearest_mkad_point).km
    return distance