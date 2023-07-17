import unittest
import requests
import json

# testing data must be adjusted to the current database


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/polygons'

    def test_provider_get(self):
        print('GET /polygons/provider')
        url = self.base_url + '/provider/64ae9932a4f893aa79954553'
        response = requests.get(
            url, headers={'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertEqual(response.json()['_id'], '64ae9932a4f893aa79954553')


if __name__ == '__main__':
    unittest.main()
