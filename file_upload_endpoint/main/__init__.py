from flask import Blueprint, request, make_response, jsonify, abort
from http import HTTPStatus
from uuid import uuid4

main = Blueprint('main', __name__)

def error_no_file(field):
    return {
        'id': uuid4(),
        'status': HTTPStatus.BAD_REQUEST,
        'title': f"[{ field }] field missing in request",
        'detail': 'Check the name of the field and that the request uses multipart/form-data encoding'
    }

def error_no_file_selection(field):
    return {
        'id': uuid4(),
        'status': HTTPStatus.BAD_REQUEST,
        'title': f"[{ field }] field value is an empty selection",
        'detail': 'Check the file selected is specified correctly and is a valid file'
    }

def error_too_large(maximum_size, request_size):
    return {
        'id': uuid4(),
        'status': HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
        'title': 'Request content_length is too great',
        'detail': 'Check the content_length of the request is less than the maximum allowed',
        'meta': {
            'maximum_content_length_allowed': maximum_size,
            'request_content_length': request_size
        }
    }

def error_wrong_mime_type(valid_mime_types, invalid_mime_type):
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
            'summary': 'Simple form action endpoint for testing file upload components in the BAS Style Kit.'
        }
    }

    return jsonify(payload)

@main.route('/upload-single', methods=['post'])
def upload_single():
    common_single_file()
    return ('', HTTPStatus.NO_CONTENT)


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

    return ('', HTTPStatus.NO_CONTENT)


@main.route('/upload-single-restricted-size', methods=['post'])
def upload_single_restricted_size():
    # Reject uploads larger than 1MB
    content_length = request.content_length
    upload_limit = 1024 * 1024  # 1MB
    if content_length is not None and content_length > upload_limit:
        payload = {'errors': [error_too_large(upload_limit, content_length)]}
        abort(make_response(jsonify(payload), HTTPStatus.REQUEST_ENTITY_TOO_LARGE))

    common_single_file()
    return ('', HTTPStatus.NO_CONTENT)


@main.route('/upload-single-restricted-mime-types', methods=['post'])
def upload_single_restricted_mime_types():
    file = common_single_file()

    file_content_type = file.content_type
    allowed_content_types = ['image/jpeg']

    if file_content_type not in allowed_content_types:
        payload = {'errors': [error_wrong_mime_type(allowed_content_types, file_content_type)]}
        abort(make_response(jsonify(payload), HTTPStatus.UNSUPPORTED_MEDIA_TYPE))

    return ('', HTTPStatus.NO_CONTENT)
