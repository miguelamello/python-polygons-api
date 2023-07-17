import unittest
import requests
import json

# testing data must be adjusted to the current database


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/polygons'

    def test_serviceareas_delete(self):
        print('DELETE /polygons/service-area')
        url = self.base_url + '/service-area/64b3170a947f1145c5a070c0'
        headers = {
            'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS', 
            'Content-Type': 'application/json'
        }
        response = requests.delete(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertIn('Service Area 64b3170a947f1145c5a070c0 deleted successfully', response.text)


if __name__ == '__main__':
    unittest.main()
