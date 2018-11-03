from http import HTTPStatus

from flask import Blueprint, abort

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
