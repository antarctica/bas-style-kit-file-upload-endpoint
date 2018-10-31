from http import HTTPStatus

from flask import Blueprint, request, make_response, jsonify, abort

from file_upload_endpoint.main.errors import error_no_file, error_no_file_selection, error_wrong_mime_type
from file_upload_endpoint.meta.errors import error_too_large


main = Blueprint('main', __name__)


def common_single_file():
    """
    Common file processing logic

    Checks a 'file' form input is included in a request and isn't an empty selection.
    Aborts the request with the appropriate error if these checks fail.
    """

    if 'file' not in request.files:
        payload = {'errors': [error_no_file('file')]}
        abort(make_response(jsonify(payload), HTTPStatus.BAD_REQUEST))

    file = request.files['file']
    if file.filename == '':
        payload = {'errors': [error_no_file_selection('file')]}
        abort(make_response(jsonify(payload), HTTPStatus.BAD_REQUEST))

    return file


@main.route("/")
def index():
    """
    Returns a simple welcome message
    """

    payload = {
        'meta': {
            'summary': 'A minimal API implementing a simple form action for testing file upload components in the BAS '
                       'Style Kit.'
        }
    }

    return jsonify(payload)


@main.route('/upload-single', methods=['post'])
def upload_single():
    """
    Accepts a single file upload

    The uploaded file is not used or stored.
    """

    common_single_file()
    return '', HTTPStatus.NO_CONTENT


@main.route('/upload-multiple', methods=['post'])
def upload_multiple():
    """
    Accepts multiple file uploads using the form array convention

    The uploaded files are not used or stored.
    """

    files = request.files.getlist('files[]')

    if len(files) <= 0:
        payload = {'errors': [error_no_file('files')]}
        abort(make_response(jsonify(payload), HTTPStatus.BAD_REQUEST))

    for file in files:
        if file.filename == '':
            payload = {'errors': [error_no_file_selection('file')]}
            abort(make_response(jsonify(payload), HTTPStatus.BAD_REQUEST))

    return '', HTTPStatus.NO_CONTENT


@main.route('/upload-single-restricted-size', methods=['post'])
def upload_single_restricted_size():
    """
    Accepts a single file upload but with an artificially small maximum file size

    Designed to prevent needing to use large files for testing when a user uploads a file that is too large.

    The uploaded file is not used or stored.
    """

    content_length = request.content_length
    upload_limit = 1024 * 40  # 40KB

    if content_length is not None and content_length > upload_limit:
        payload = {'errors': [error_too_large(upload_limit, content_length)]}
        abort(make_response(jsonify(payload), HTTPStatus.REQUEST_ENTITY_TOO_LARGE))

    common_single_file()
    return '', HTTPStatus.NO_CONTENT


@main.route('/upload-single-restricted-mime-types', methods=['post'])
def upload_single_restricted_mime_types():
    """
    Accepts a single file upload but with an artificially limited set of allowed MIME types

    Designed to more easily test when a user uploads an unsupported file type.

    The uploaded file is not used or stored.
    """

    file = common_single_file()

    file_content_type = file.content_type
    allowed_content_types = ['image/jpeg']

    if file_content_type not in allowed_content_types:
        payload = {'errors': [error_wrong_mime_type(allowed_content_types, file_content_type)]}
        abort(make_response(jsonify(payload), HTTPStatus.UNSUPPORTED_MEDIA_TYPE))

    return '', HTTPStatus.NO_CONTENT
