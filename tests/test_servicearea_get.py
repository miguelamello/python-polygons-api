import unittest
import requests
import json

# testing data must be adjusted to the current database


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/polygons'

    def test_servicearea_get(self):
        print('GET /polygons/service-area')
        url = self.base_url + '/service-area/64b316f5947f1145c5a070bf'
        response = requests.get(url, headers={'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertEqual(response.json()['_id'], '64b316f5947f1145c5a070bf')


if __name__ == '__main__':
    unittest.main()
