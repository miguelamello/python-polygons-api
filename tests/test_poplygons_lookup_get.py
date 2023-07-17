import unittest
import requests
import json

# testing data must be adjusted to the current database

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/polygons'

    def test_poplygons_lookup_get(self):
        print('GET /polygons/lookup')
        url = self.base_url + '/lookup?longitude=-74.0159&latitude=40.7161'
        headers = {
            'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS'
        }
        response = requests.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertIsInstance(response.json(), list)


if __name__ == '__main__':
    unittest.main()
