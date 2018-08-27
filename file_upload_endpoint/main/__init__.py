from http import HTTPStatus

from flask import Blueprint, request, make_response, jsonify, abort, current_app as app

from file_upload_endpoint.main.errors import error_no_file, error_no_file_selection, error_too_large, \
        error_wrong_mime_type

main = Blueprint('main', __name__)


def common_single_file():
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
    payload = {
        'meta': {
            'summary': 'A minimal API implementing a simple form action for testing file upload components in the BAS '
                       'Style Kit. '
        }
    }

    return jsonify(payload)


@main.route('/upload-single', methods=['post'])
def upload_single():
    common_single_file()
    return '', HTTPStatus.NO_CONTENT


@main.route('/upload-multiple', methods=['post'])
def upload_multiple():
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
    content_length = request.content_length
    upload_limit = 1024 * 40  # 40KB

    if content_length is not None and content_length > upload_limit:
        payload = {'errors': [error_too_large(upload_limit, content_length)]}
        abort(make_response(jsonify(payload), HTTPStatus.REQUEST_ENTITY_TOO_LARGE))

    common_single_file()
    return '', HTTPStatus.NO_CONTENT


@main.route('/upload-single-restricted-mime-types', methods=['post'])
def upload_single_restricted_mime_types():
    file = common_single_file()

    file_content_type = file.content_type
    allowed_content_types = ['image/jpeg']

    if file_content_type not in allowed_content_types:
        payload = {'errors': [error_wrong_mime_type(allowed_content_types, file_content_type)]}
        abort(make_response(jsonify(payload), HTTPStatus.UNSUPPORTED_MEDIA_TYPE))

    return '', HTTPStatus.NO_CONTENT
