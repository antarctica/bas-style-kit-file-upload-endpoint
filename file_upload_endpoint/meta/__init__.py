from http import HTTPStatus

from cerberus import Validator
from flask import Blueprint, abort, current_app as app, jsonify, make_response

from file_upload_endpoint.meta.errors import error_request_validation
from file_upload_endpoint.meta.utils import get_cerberus_schema

meta = Blueprint('meta', __name__)


@meta.route('/meta/health/canary', methods=['get', 'options'])
def meta_healthcheck_canary():
    """
    Returns a 2XX response when this service is healthy

    As this API has no dependencies the service is healthy if this function can be executed
    """
    return '', HTTPStatus.NO_CONTENT


@meta.route('/meta/errors/generic-bad-request')
def meta_errors_generic_bad_request():
    """
    Simulates a bad request
    """
    abort(HTTPStatus.BAD_REQUEST)


@meta.route('/meta/errors/generic-internal-server-error')
def meta_errors_generic_internal_server_error():
    """
    Simulates an internal error
    """
    abort(HTTPStatus.INTERNAL_SERVER_ERROR)


@meta.route('/meta/logging/entries/<logging_level>', methods=['post'])
def meta_logging_entry(logging_level: str):
    """
    Simulates logging a message using the application logger at a given severity

    The message logged is hard-coded to allow for automated testing

    :type logging_level: str
    :param logging_level: severity to log the message at (required parameter)
    """

    # Validate request
    logging_entry_schema = {
        'logging_level': {
            'type': 'string',
            'request_type': 'parameter',
            'required': True,
            'allowed': ['debug', 'info', 'warning', 'error', 'critical']
        }
    }
    logging_entry_document = {'logging_level': logging_level}
    validator = Validator(get_cerberus_schema(logging_entry_schema))
    if not validator.validate(logging_entry_document):
        payload = {'errors': error_request_validation(validator, logging_entry_schema)}
        abort(make_response(jsonify(payload), HTTPStatus.BAD_REQUEST))

    # Log message
    if logging_level == 'debug':
        app.logger.debug('debug log message - from logging meta endpoint')
    elif logging_level == 'info':
        app.logger.info('info log message - from logging meta endpoint')
    elif logging_level == 'warning':
        app.logger.warning('warning log message - from logging meta endpoint')
    elif logging_level == 'error':
        app.logger.error('error log message - from logging meta endpoint')
    elif logging_level == 'critical':
        app.logger.critical('critical log message - from logging meta endpoint')

    return '', HTTPStatus.ACCEPTED
