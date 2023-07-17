import unittest
import requests, json

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:8000/polygons'

    def test_app_doc(self):
        print('.Test the API documentation page')
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'text/html; charset=utf-8')
        self.assertIn('<title>Polygons Reference</title>', response.text)
        
    def test_provider_get(self):
        print('Test GET /polygons/provider')
        url = self.base_url + '/provider/64ae9932a4f893aa79954553'
        response = requests.get(url, headers={'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertEqual(response.json()['_id'], '64ae9932a4f893aa79954553')
        
    def test_provider_post(self):
        print('Test POST /polygons/provider')
        url = self.base_url + '/provider'
        headers = {
            'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS', 
            'Content-Type': 'application/json'
        }
        data = {
            "name": "MMM Shuttle",
            "email": "info@mmmshuttle.com",
            "phone": "037847228",
            "language": "English",
            "currency": "USD"
        }
        response = requests.post(url, headers=headers, data=data)
        #self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.headers['content-type'], 'application/json')
        #self.assertEqual(response.json()['_id'], '64ae9932a4f893aa79954553')
        print(response.text)

if __name__ == '__main__':
    unittest.main()

