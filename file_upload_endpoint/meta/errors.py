from http import HTTPStatus
from uuid import uuid4

import sentry_sdk
from flask import request, make_response, jsonify, current_app as app


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


def error_too_large(maximum_size, request_size):
    log_message = f"Request content length, [{ request_size }], is too great"
    app.logger.warning(log_message)

    # as the API handles this error with this error message it is not reported to Sentry
    # however, because it's useful for tracking, an event is sent anyway.
    with sentry_sdk.push_scope() as scope:
        scope.set_extra('debug', False)
        sentry_sdk.capture_message(log_message)

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


# noinspection PyUnusedLocal
def error_handler_generic_bad_request(e):
    payload = {'errors': [error_generic_bad_request()]}
    return make_response(jsonify(payload), HTTPStatus.BAD_REQUEST)


# noinspection PyUnusedLocal
def error_handler_generic_not_found(e):
    payload = {'errors': [error_generic_not_found()]}
    return make_response(jsonify(payload), HTTPStatus.NOT_FOUND)


# noinspection PyUnusedLocal
def error_handler_generic_internal_server_error(e):
    payload = {'errors': [error_generic_internal_server_error()]}
    return make_response(jsonify(payload), HTTPStatus.INTERNAL_SERVER_ERROR)


# noinspection PyUnusedLocal
def error_handler_request_entity_too_large(e):
    content_length = request.content_length
    upload_limit = app.config['MAX_CONTENT_LENGTH']
    payload = {'errors': [error_too_large(upload_limit, content_length)]}
    return make_response(jsonify(payload), HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
