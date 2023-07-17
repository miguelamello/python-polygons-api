import unittest
import requests, json

# testing data must be adjusted to the current database

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/polygons'

    def test_app_doc(self):
        print('.API documentation page')
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'text/html; charset=utf-8')
        self.assertIn('<title>Polygons Reference</title>', response.text)
        
    def test_provider_get(self):
        print('GET /polygons/provider')
        url = self.base_url + '/provider/64ae9932a4f893aa79954553'
        response = requests.get(url, headers={'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertEqual(response.json()['_id'], '64ae9932a4f893aa79954553')
        
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
        
    def test_provider_put(self):
        print('PUT /polygons/provider')
        url = self.base_url + '/provider/64ae9932a4f893aa79954553'
        headers = {
            'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS', 
            'Content-Type': 'application/json'
        }
        data = {
            "name": "MNO Ltd",
            "email": "mno@example.com",
            "phone": "0123456789",
            "language": "German",
            "currency": "CAD"
        }
        response = requests.put(url, headers=headers, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertIn('Provider 64ae9932a4f893aa79954553 updated successfully', response.text)
        
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
        self.assertIn('Provider 64ae9932a4f893aa79954553 deleted successfully', response.text)
        
    def test_provider_serviceareas_get(self):
        print('GET /polygons/provider/service-areas')
        url = self.base_url + '/provider/service-areas/64ae993ca4f893aa79954553'
        response = requests.get(url, headers={'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertIsInstance(response.json(), list)
        
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
        
    def test_servicearea_get(self):
        print('GET /polygons/service-area')
        url = self.base_url + '/service-area/64b316f5947f1145c5a070bf'
        response = requests.get(url, headers={'Api-key': 'BvAEfTYaVkHw06IR6l2WfEKJCpXOtMwS'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertEqual(response.json()['_id'], '64b316f5947f1145c5a070bf')
        
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

