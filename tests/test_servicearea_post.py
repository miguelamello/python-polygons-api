import unittest
import requests
import json

# testing data must be adjusted to the current database


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/polygons'

    def test_servicearea_post(self):
        print('POST /polygons/service-area')
        url = self.base_url + '/service-area'
        headers = {
            'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS', 
            'Content-Type': 'application/json'
        }
        data = {
            "name": "Madson Square Garden",
            "price": 27.43,
            "vertices": {
                "type": "Polygon",
                "coordinates": [
                [[-74.01555, 40.7123], [-74.0055, 40.7161], [-74.0055, 40.7103], [-74.0159, 40.7103], [-74.01555, 40.7123]]
                ]
            },
            "provider": "64ae995aa4f893aa79954557"
        }
        response = requests.post(url, headers=headers, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertIn('Service Area created successfully', response.text)


if __name__ == '__main__':
    unittest.main()
