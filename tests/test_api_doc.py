import unittest
import requests, json

# testing data must be adjusted to the current database

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/polygons'

    def test_api_doc(self):
        print('.API documentation page')
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'text/html; charset=utf-8')
        self.assertIn('<title>Polygons Reference</title>', response.text)


if __name__ == '__main__':
    unittest.main()

