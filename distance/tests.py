import unittest

import requests

from views import distance


class TestFlask(unittest.TestCase):

    def test_main(self):
        """Тест на то что страница отображается"""
        with distance.test_client() as client:
            result: requests.models.Response = client.get('/')
            self.assertEqual(result.status_code, 200)

    def test_distance_page_loads(self):
        """Тест на корректное отображение html документа"""
        with distance.test_client() as client:
            result: requests.models.Response = client.get('/')
            statement: bytes = bytes(
                "Расчет дистанции до ближайшей точки на МКАД", 'utf-8')
            self.assertTrue(statement in result.data)

    def test_inside_mkad_doesnt_count_distance(self):
        """Тест на передачу объекта внутри МКАД"""
        with distance.test_client() as client:
            result: requests.models.Response = client.post(
                '/', data=dict(query="Москва, Кремль"))
            query_result: bytes = bytes('Объект внутри МКАД', 'utf-8')
            self.assertTrue(query_result in result.data)

    def test_outside_mkad_counts_distance(self):
        """Тест на передачу объекта вне МКАД"""
        with distance.test_client() as client:
            result: requests.models.Response = client.post(
                '/', data=dict(query="Алматы, Абая 21"))
            query_result: bytes = bytes('3099', 'utf-8')
            self.assertTrue(query_result in result.data)
