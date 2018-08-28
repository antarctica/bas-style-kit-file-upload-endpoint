import os
import unittest

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

    def common_preflight(self, path):
        response = self.client.options(path, headers={'origin': 'https://style-kit.web.bas.ac.uk'})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('access-control-allow-origin', response.headers)
        self.assertEqual('https://style-kit.web.bas.ac.uk', response.headers['access-control-allow-origin'])
        self.assertIn('allow', response.headers)
        self.assertEqual(['OPTIONS', 'POST'], sorted(response.headers['allow'].split(', ')))

    def test_index(self):
        response = self.client.get('/')
        json_response = response.get_json()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('meta', json_response.keys())
        self.assertIn('summary', json_response['meta'].keys())

    def test_upload_single(self):
        with open(os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'valid.png'), 'rb') as file_upload: 
            request_data = {
                'file': (file_upload, file_upload.name)
            }
            response = self.client.post(
                '/upload-single', 
                content_type='multipart/form-data', 
                data=request_data
            )
            self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_upload_single_preflight(self):
        self.common_preflight('/upload-single')

    def test_upload_multiple(self):
        with open(os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'valid.png'), 'rb') as file_upload: 
            request_data = {
                'files[]': (file_upload, file_upload.name)
            }
            response = self.client.post(
                '/upload-multiple', 
                content_type='multipart/form-data', 
                data=request_data
            )
            self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_upload_multiple_preflight(self):
        self.common_preflight('/upload-multiple')

    def test_upload_single_restricted_size(self):
        expected_error = {
            'detail': 'Check the content length of the request is less than the maximum allowed',
            'id': 'a611b89f-f1bb-43c5-8efa-913c83c9109e',
            'status': 413,
            'meta': {
                'maximum_content_length_allowed': 40960,
                'request_content_length': 44174
            },
            'title': 'Request content length is too great'
        }

        with open(os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'invalid.png'), 'rb') as file_upload: 
            request_data = {
                'file': (file_upload, file_upload.name)
            }
            response = self.client.post(
                '/upload-single-restricted-size', 
                content_type='multipart/form-data', 
                data=request_data
            )
            json_response = response.get_json()
            self.assertEqual(response.status_code, HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
            self.assertIn('errors', json_response.keys())
            self.assertEqual(len(json_response['errors']), 1)
            
            # Overwrite dynamic error ID with static value to allow comparision
            if 'id' in json_response['errors'][0].keys():
                json_response['errors'][0]['id'] = 'a611b89f-f1bb-43c5-8efa-913c83c9109e'
            
            # Overwrite dynamic content length with static value (as it is made up of more than just the upload file)
            if 'meta' in json_response['errors'][0].keys():
                if 'request_content_length' in json_response['errors'][0]['meta'].keys():
                    if json_response['errors'][0]['meta']['request_content_length'] > 40960:
                        json_response['errors'][0]['meta']['request_content_length'] = 44174

            self.assertDictEqual(json_response['errors'][0], expected_error)
    
    def test_upload_single_preflight(self):
        self.common_preflight('/upload-single-restricted-size')

    def test_upload_single_restricted_mime_types(self):
        expected_error = {
            'detail': 'Check the file mime_type is in the list of allowed types',
            'id': 'a611b89f-f1bb-43c5-8efa-913c83c9109e',
            'status': 415,
            'meta': {
                'allowed_mime_types': ['image/jpeg'],
                'instance_mime_type': 'image/png'
            },
            'title': 'File type uploaded is not allowed'
        }

        with open(os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'invalid.png'), 'rb') as file_upload: 
            request_data = {
                'file': (file_upload, file_upload.name)
            }
            response = self.client.post(
                '/upload-single-restricted-mime-types', 
                content_type='multipart/form-data', 
                data=request_data
            )
            json_response = response.get_json()
            self.assertEqual(response.status_code, HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
            self.assertIn('errors', json_response.keys())
            self.assertEqual(len(json_response['errors']), 1)
            
            # Overwrite dynamic error ID with static value to allow comparision
            if 'id' in json_response['errors'][0].keys():
                json_response['errors'][0]['id'] = 'a611b89f-f1bb-43c5-8efa-913c83c9109e'
            
            self.assertDictEqual(json_response['errors'][0], expected_error)
    
    def test_upload_single_restricted_mime_types_preflight(self):
        self.common_preflight('/upload-single-restricted-mime-types')
