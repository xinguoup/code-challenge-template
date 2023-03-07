import os
import sys
import requests
import unittest

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(basedir, ".."))

import db_utils


class TestSQL(unittest.TestCase):
    def setUp(self):
        self.where_condition_1 = [("station_id", "110072"), ("date(date)", "1985-01-01")]
        self.where_condition_2 = [("station_id", "110072"), ("year", "1985")]
        self.limit=20
        self.offset=0

    def test_generate_where_clause(self):
        res = db_utils.generate_where_clause(self.where_condition_1)
        self.assertEqual(res, "WHERE station_id='110072' AND date(date)='1985-01-01' ")

    def test_generate_page_clause(self):
        res = db_utils.generate_page_clause()
        self.assertEqual(res, "limit 10 offset 0 ")

        res = db_utils.generate_page_clause(limit=self.limit, offset=self.offset)
        self.assertEqual(res, "limit 20 offset 0 ")

    def test_get_data_wheather_record(self):
        res = db_utils.get_data_wheather_record_by_station_id_and_date(self.where_condition_1, self.limit, self.offset)
        self.assertEqual(res, [{'station_id': 110072, 'date': '1985-01-01', 'max_temperature': -2.2, 'min_temperature': -12.8, 'precipitation_amount': 9.4}])

        res = db_utils.get_data_wheather_record_by_station_id_and_date(self.where_condition_1)
        self.assertEqual(res, [{'station_id': 110072, 'date': '1985-01-01', 'max_temperature': -2.2, 'min_temperature': -12.8, 'precipitation_amount': 9.4}])
     
    def test_get_data_avg_report(self):
        res = db_utils.get_data_avg_report_by_station_id_and_year(self.where_condition_2, self.limit, self.offset)
        self.assertEqual(res, [{'station_id': 110072, 'year': 1985, 'avg_max_temperature': 15.33, 'avg_min_temperature': -1.18, 'precipitation_total': 78.01}])
 

class TestApp(unittest.TestCase):
    def setUp(self):
        from problem4.app import create_app
        from multiprocessing import Process
        self.server = Process(target=create_app, args=())
        self.server.start()
        self.host = "http://127.0.0.1:5000"

    def tearDown(self):
        self.server.terminate()

    def test_weather_api_without_param(self):
        response = requests.get(self.host + "/api/weather")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["err_msg"], "station_id or date must set one")

    def test_weather_api(self):
        response = requests.get(self.host + "/api/weather?station_id=110072&date=19850101")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, {"code": 0, "err_msg": "", "data": [{"station_id": 110072, "date": "1985-01-01", "max_temperature": -2.2, "min_temperature": -12.8, "precipitation_amount": 9.4}]})

    def test_weather_api_without_param(self):
        response = requests.get(self.host + "/api/weather/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["err_msg"], "station_id or year must set one")

    def test_weather_api_without_param(self):
        response = requests.get(self.host + "/api/weather/stats?station_id=110072&year=1992")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, {"code": 0, "err_msg": "", "data": [{"station_id": 110072, "year": 1992, "avg_max_temperature": 6.67, "avg_min_temperature": -5.95, "precipitation_total": -106.72}]})

  
if __name__ == '__main__':
    unittest.main()