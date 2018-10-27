from http import HTTPStatus

from flask import Blueprint, abort

meta = Blueprint('meta', __name__)


@meta.route('/meta/errors/generic-bad-request')
def meta_errors_generic_bad_request():
    abort(HTTPStatus.BAD_REQUEST)


@meta.route('/meta/errors/generic-internal-server-error')
def meta_errors_generic_internal_server_error():
    abort(HTTPStatus.INTERNAL_SERVER_ERROR)
