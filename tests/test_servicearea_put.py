import unittest
import requests
import json

# testing data must be adjusted to the current database


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/polygons'

    def test_servicearea_put(self):
        print('PUT /polygons/service-area')
        url = self.base_url + '/service-area/64b316f5947f1145c5a070bf'
        headers = {
            'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS', 
            'Content-Type': 'application/json'
        }
        data = {
            "name": "East Village",
            "price": 18.34,
            "vertices": {
                "type": "Polygon",
                "coordinates": [[
                    [-73.9889,40.7306],
                    [-73.9826,40.7306],
                    [-73.9826,40.7234],
                    [-73.9889,40.7234],
                    [-73.9889,40.7306]
                ]]
            },
            "provider": "64ae993ca4f893aa79954554"
        }
        response = requests.put(url, headers=headers, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertIn('Service Area 64b316f5947f1145c5a070bf updated successfully', response.text)


if __name__ == '__main__':
    unittest.main()
