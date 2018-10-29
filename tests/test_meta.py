import os
import unittest

from http import HTTPStatus

from file_upload_endpoint import create_app


class MetaBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_meta_errors_generic_bad_request(self):
        expected_error = {
            'detail': 'No additional information is available, check your request and try again',
            'id': 'a611b89f-f1bb-43c5-8efa-913c83c9109e',
            'status': 400,
            'title': 'Bad Request'
        }

        response = self.client.get('/meta/errors/generic-bad-request')
        json_response = response.get_json()
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn('errors', json_response.keys())
        self.assertEqual(len(json_response['errors']), 1)

        # Overwrite dynamic error ID with static value to allow comparision
        if 'id' in json_response['errors'][0].keys():
            json_response['errors'][0]['id'] = 'a611b89f-f1bb-43c5-8efa-913c83c9109e'

        self.assertDictEqual(json_response['errors'][0], expected_error)

    def test_meta_errors_generic_not_found(self):
        expected_error = {
            'detail': 'The requested URL was not found, check the address and try again',
            'id': 'a611b89f-f1bb-43c5-8efa-913c83c9109e',
            'status': 404,
            'title': 'Not Found'
        }

        response = self.client.get('/meta/errors/generic-not-found')
        json_response = response.get_json()
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIn('errors', json_response.keys())
        self.assertEqual(len(json_response['errors']), 1)

        # Overwrite dynamic error ID with static value to allow comparision
        if 'id' in json_response['errors'][0].keys():
            json_response['errors'][0]['id'] = 'a611b89f-f1bb-43c5-8efa-913c83c9109e'

        self.assertDictEqual(json_response['errors'][0], expected_error)

    def test_meta_errors_generic_internal_server_error(self):
        expected_error = {
            'detail': 'No additional information is available, please try again in a few minutes or seek support',
            'id': 'a611b89f-f1bb-43c5-8efa-913c83c9109e',
            'status': 500,
            'title': 'Internal Server Error'
        }

        response = self.client.get('/meta/errors/generic-internal-server-error')
        json_response = response.get_json()
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertIn('errors', json_response.keys())
        self.assertEqual(len(json_response['errors']), 1)

        # Overwrite dynamic error ID with static value to allow comparision
        if 'id' in json_response['errors'][0].keys():
            json_response['errors'][0]['id'] = 'a611b89f-f1bb-43c5-8efa-913c83c9109e'

        self.assertDictEqual(json_response['errors'][0], expected_error)
