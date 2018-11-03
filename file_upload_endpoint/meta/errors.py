from http import HTTPStatus
from uuid import uuid4

import sentry_sdk
from cerberus import Validator
from cerberus.errors import ValidationError  # noqa: F401
from flask import request, make_response, jsonify, current_app as app


def error_generic_bad_request() -> dict:
    """
    Creates a generic request error

    :rtype: dict
    :return: Complete JSON-API compatible error object
    """
    return {
        'id': uuid4(),
        'status': HTTPStatus.BAD_REQUEST,
        'title': 'Bad Request',
        'detail': 'No additional information is available, check your request and try again'
    }


def error_generic_not_found() -> dict:
    """
    Creates a generic 'not found' error

    :rtype: dict
    :return: Complete JSON-API compatible error object
    """
    return {
        'id': uuid4(),
        'status': HTTPStatus.NOT_FOUND,
        'title': 'Not Found',
        'detail': 'The requested URL was not found, check the address and try again'
    }


def error_generic_internal_server_error() -> dict:
    """
    Creates a generic internal error

    :rtype: dict
    :return: Complete JSON-API compatible error object
    """
    return {
        'id': uuid4(),
        'status': HTTPStatus.INTERNAL_SERVER_ERROR,
        'title': 'Internal Server Error',
        'detail': 'No additional information is available, please try again in a few minutes or seek support'
    }


def error_too_large(maximum_size: int, request_size: int) -> dict:
    """
    Creates a 'request too big' error

    :type maximum_size: int
    :param maximum_size: Maximum content length (in bytes)

    :type request_size: int
    :param request_size: Content length of request (in bytes)

    :rtype: dict
    :return: Complete JSON-API compatible error object
    """
    log_message = f"Request content length, [{ request_size }], is too great"
    app.logger.warning(log_message)

    # As the API handles this error through this error message, it is not reported to Sentry.
    # However, because it's useful for tracking, we want report it anyway.
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
            'request_content_length': request_size,
            'content_length_units': 'bytes'
        }
    }


def error_request_validation(validator: Validator, schema: dict) -> list:
    """
    Generates errors for each invalid field in a validation schema

    This function returning errors for end-users when a Cerberus validator returns False. Cerberus is a Python
    validation library, http://docs.python-cerberus.org, it uses a schema mapping (dict) to define validation
    requirements.

    This function accepts a Cerberus validator and loops through its errors. Cerberus structures errors by schema field,
    which this function flattens. For each error a standard set of information is extracted. For some validation rules,
    additional context is added such as lists of allowed values.

    To improve the errors returned to end-users, this application uses an extended validation schema that cannot be
    used by Cerberus and needs to provided separately. This extended schema describes, for example, whether a 'field'
    is a request parameter, query parameter, header, body field, etc.

    :type validator: Validator
    :param validator: Cerberus validator object

    :type schema: dict
    :param schema: Extended (application) validation schema

    :rtype: list
    :return: List of complete, JSON-API compatible error objects
    """

    validation_errors = []

    # We can't iterate validator.document_error_tree directly as a dict of ValidatorError's, we therefore check whether
    # each field in the validation schema has any errors and loop through them.
    for schema_field in validator.schema.keys():
        if schema_field in validator.document_error_tree:
            for validator_error in validator.document_error_tree[schema_field]:  # type:ValidationError
                # Base error information
                validation_error = {
                    'id': uuid4(),
                    'status': HTTPStatus.BAD_REQUEST,
                    'title': 'Request validation error',
                    'detail': f"Invalid value for { schema[schema_field]['request_type'] } [{ schema_field }], "
                              f"check your request and try again",
                    'meta': {
                        schema[schema_field]['request_type']: schema_field,
                        'invalid_value': validator_error.value
                    }
                }

                # Enrich certain types of validation error based on the validation rule
                if validator_error.rule == 'allowed':
                    validation_error['detail'] = f"Value for { schema[schema_field]['request_type'] } " \
                        f"[{ schema_field }] invalid, check your request against the allowed values and try again"
                    validation_error['meta']['allowed_values'] = validator_error.constraint

                validation_errors.append(validation_error)

    return validation_errors


# noinspection PyUnusedLocal
def error_handler_generic_bad_request(e: Exception):
    """
    Flask error handler for '400 Bad Request' errors

    :type e: Exception
    :param e: Exception

    :return: Flask response
    """
    payload = {'errors': [error_generic_bad_request()]}
    return make_response(jsonify(payload), HTTPStatus.BAD_REQUEST)


# noinspection PyUnusedLocal
def error_handler_generic_not_found(e: Exception):
    """
    Flask error handler for '404 Not Found' errors

    :type e: Exception
    :param e: Exception

    :return: Flask response
    """
    payload = {'errors': [error_generic_not_found()]}
    return make_response(jsonify(payload), HTTPStatus.NOT_FOUND)


# noinspection PyUnusedLocal
def error_handler_generic_internal_server_error(e: Exception):
    """
    Flask error handler for '500 Internal Server Error' errors

    :type e: Exception
    :param e: Exception

    :return: Flask response
    """
    payload = {'errors': [error_generic_internal_server_error()]}
    return make_response(jsonify(payload), HTTPStatus.INTERNAL_SERVER_ERROR)


# noinspection PyUnusedLocal
def error_handler_request_entity_too_large(e: Exception):
    """
    Flask error handler for '413 Request Entity Too Large' errors

    :type e: Exception
    :param e: Exception

    :return: Flask response
    """
    content_length = request.content_length
    upload_limit = app.config['MAX_CONTENT_LENGTH']
    payload = {'errors': [error_too_large(upload_limit, content_length)]}
    return make_response(jsonify(payload), HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
