import unittest
import requests
import json

# testing data must be adjusted to the current database


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/polygons'

    def test_provider_serviceareas_delete(self):
        print('DELETE /polygons/provider/service-areas')
        url = self.base_url + '/provider/service-areas/64ae995aa4f893aa79954557'
        headers = {
            'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS', 
            'Content-Type': 'application/json'
        }
        response = requests.delete(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertIn('Service Areas from provider 64ae995aa4f893aa79954557 deleted successfully', response.text)


if __name__ == '__main__':
    unittest.main()
