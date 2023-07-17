import unittest
import requests
import json

# testing data must be adjusted to the current database


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/polygons'

    def test_provider_serviceareas_get(self):
        print('GET /polygons/provider/service-areas')
        url = self.base_url + '/provider/service-areas/64ae993ca4f893aa79954553'
        response = requests.get(url, headers={'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertIsInstance(response.json(), list)


if __name__ == '__main__':
    unittest.main()
