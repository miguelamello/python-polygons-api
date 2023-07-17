import unittest
import requests
import json

# testing data must be adjusted to the current database


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/polygons'

    def test_provider_delete(self):
        print('DELETE /polygons/provider')
        url = self.base_url + '/provider/64ae9932a4f893aa79954553'
        headers = {
            'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS',
            'Content-Type': 'application/json'
        }
        response = requests.delete(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertIn(
            'Provider 64ae9932a4f893aa79954553 deleted successfully', response.text)


if __name__ == '__main__':
    unittest.main()
