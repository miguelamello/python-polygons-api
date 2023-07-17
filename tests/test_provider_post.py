import unittest
import requests
import json

# testing data must be adjusted to the current database


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/polygons'
        

    def test_provider_post(self):
        print('POST /polygons/provider')
        url = self.base_url + '/provider'
        headers = {
            'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS',
            'Content-Type': 'application/json'
        }
        data = {
            "name": "PQP Shuttle",
            "email": "info@pqpshuttle.com",
            "phone": "028364811",
            "language": "English",
            "currency": "USD"
        }
        response = requests.post(url, headers=headers, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertIn('id', response.text)


if __name__ == '__main__':
    unittest.main()
