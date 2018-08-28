from http import HTTPStatus
from uuid import uuid4

from flask import request, make_response, jsonify, abort, current_app as app

def error_generic_bad_request():
    return {
        'id': uuid4(),
        'status': HTTPStatus.BAD_REQUEST,
        'title': 'Bad Request',
        'detail': 'No additional information is available, check your request and try again'
    }

def error_generic_not_found():
    return {
        'id': uuid4(),
        'status': HTTPStatus.NOT_FOUND,
        'title': 'Not Found',
        'detail': 'The requested URL was not found, check the address and try again'
    }

def error_generic_internal_server_error():
    return {
        'id': uuid4(),
        'status': HTTPStatus.INTERNAL_SERVER_ERROR,
        'title': 'Internal Server Error',
        'detail': 'No additional information is available, please try again in a few minutes or seek support'
    }

def error_no_file(field):
    app.logger.warning(f"[{ field }] field missing in request")

    return {
        'id': uuid4(),
        'status': HTTPStatus.BAD_REQUEST,
        'title': f"[{ field }] field missing in request",
        'detail': 'Check the name of the field and that the request uses multipart/form-data encoding'
    }


def error_no_file_selection(field):
    app.logger.warning(f"[{ field }] field value is an empty selection")

    return {
        'id': uuid4(),
        'status': HTTPStatus.BAD_REQUEST,
        'title': f"[{ field }] field value is an empty selection",
        'detail': 'Check the file selected is specified correctly and is a valid file'
    }


def error_too_large(maximum_size, request_size):
    app.logger.warning(f"Request content length, [{ request_size }], is too great")

    return {
        'id': uuid4(),
        'status': HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
        'title': 'Request content length is too great',
        'detail': 'Check the content length of the request is less than the maximum allowed',
        'meta': {
            'maximum_content_length_allowed': maximum_size,
            'request_content_length': request_size
        }
    }


def error_wrong_mime_type(valid_mime_types, invalid_mime_type):
    app.logger.warning(f"File type uploaded, [{ invalid_mime_type }], is not allowed")

    return {
        'id': uuid4(),
        'status': HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        'title': 'File type uploaded is not allowed',
        'detail': 'Check the file mime_type is in the list of allowed types',
        'meta': {
            'allowed_mime_types': valid_mime_types,
            'instance_mime_type': invalid_mime_type
        }
    }


def error_handler_request_entity_too_large(e):
    content_length = request.content_length
    upload_limit = app.config['MAX_CONTENT_LENGTH']
    payload = {'errors': [error_too_large(upload_limit, content_length)]}
    return make_response(jsonify(payload), HTTPStatus.REQUEST_ENTITY_TOO_LARGE)


def error_handler_generic_bad_request(e):
    payload = {'errors': [error_generic_bad_request()]}
    return make_response(jsonify(payload), HTTPStatus.BAD_REQUEST)


def error_handler_generic_not_found(e):
    payload = {'errors': [error_generic_not_found()]}
    return make_response(jsonify(payload), HTTPStatus.NOT_FOUND)


def error_handler_generic_internal_server_error(e):
    payload = {'errors': [error_generic_internal_server_error()]}
    return make_response(jsonify(payload), HTTPStatus.INTERNAL_SERVER_ERROR)
