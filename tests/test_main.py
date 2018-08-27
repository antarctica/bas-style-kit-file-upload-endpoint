import unittest
import json

from http import HTTPStatus

from file_upload_endpoint import create_app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        json_response = json.loads(response.get_data())
        self.assertIn('meta', json_response.keys())
        self.assertIn('summary', json_response['meta'].keys())
