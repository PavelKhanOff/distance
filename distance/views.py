"""Расскомментируй код снизу, чтобы создать blueprint"""
import logging
from typing import List

from flask import Blueprint, render_template, request

from .additional_functions import (find_closest_lat_lon, get_distance,
                                   get_lat_and_long, is_in_mkad)

distance = Blueprint(
    'distance', __name__, url_prefix='/distance', template_folder='templates')

"""Расскомментируй код снизу, чтобы создать приложение для прогонки
 тестов либо использования приложения как главное приложение,
 обратите внимание что url изменится на '/'"""
# import logging
# from typing import List
#
# from flask import Flask, render_template, request
#
# from .additional_functions import (find_closest_lat_lon, get_distance,
#                                    get_lat_and_long, is_in_mkad)
#
# distance = Flask(__name__)
#
# logging.basicConfig(filename='.log',
# level=logging.DEBUG,
# format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@distance.route('/', methods=['POST', 'GET'])
def get_distance_lat_long():
    """Логика расчета и отображения html по адресу '/distance'"""
    if request.method == 'POST':
        try:
            query: str = request.form['query']
            query_coordinates: List = get_lat_and_long(query)
            if is_in_mkad(query_coordinates):
                words: str = 'Объект внутри МКАД'
                return render_template('distance.html', words=words)
            nearest_mkad_point: List = find_closest_lat_lon(query_coordinates)
            distance_between_points: float = get_distance(
                query_coordinates, nearest_mkad_point)
            return render_template(
                'distance.html', distance=round(distance_between_points, 2))
        except Exception:
            message: str = (
                'К сожалению, мы не можем найти введенный адрес, '
                'попробуйте ввести адрес подробнее')
            logging.exception(msg='Адрес поиска не найден.')
            return render_template('distance.html', message=message)
    return render_template('distance.html')
