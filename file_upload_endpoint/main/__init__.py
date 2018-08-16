from flask import Blueprint, request, jsonify, abort
from http import HTTPStatus
from uuid import uuid4

main = Blueprint('main', __name__)

def error_no_file(field):
    return {
        'id': uuid4(),
        'status': HTTPStatus.BAD_REQUEST,
        'title': f"[{ field }] field missing in request",
        'detail': 'Check the name of the field and that the request is multipart/form-data'
    }

def error_no_file_selection(field):
    return {
        'id': uuid4(),
        'status': HTTPStatus.BAD_REQUEST,
        'title': f"[{ field }] field value is an empty selection",
        'detail': 'Check the file selected is specified correctly and is a valid file'
    }

def error_too_large(maximum_size):
    return {
        'id': uuid4(),
        'status': HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
        'title': 'The file uploaded is too large',
        'detail': 'Check the contnet_length of the request is less than the maximum allowed',
        'meta': {
            'maximum_content_length_allowed': maximum_size
        }
    }

def error_wrong_mime_type(valid_mime_types, invalid_mime_type):
    return {
        'id': uuid4(),
        'status': HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        'title': 'The file type uploaded is not allowed',
        'detail': 'check the mime_type of the file is in the list of allowed types',
        'meta': {
            'allowed_mime_types': valid_mime_types,
            'instance_mime_type': invalid_mime_type
        }
    }

def common_single_file():
    if 'file' not in request.files:
        payload = {'errors': [error_no_file('file')]}
        return jsonify(payload), HTTPStatus.BAD_REQUEST

    file = request.files['file']
    if file.filename == '':
        payload = {'errors': [error_no_file_selection('file')]}
        return jsonify(payload), HTTPStatus.BAD_REQUEST

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
        return jsonify(payload), HTTPStatus.BAD_REQUEST

    for file in files:
        if file.filename == '':
            payload = {'errors': [error_no_file_selection('file')]}
            return jsonify(payload), HTTPStatus.BAD_REQUEST

    return ('', HTTPStatus.NO_CONTENT)


@main.route('/upload-single-restricted-size', methods=['post'])
def upload_single_restricted_size():
    # Reject uploads larger than 1MB
    content_length = request.content_length
    upload_limit = 1024 * 1024  # 1MB
    if content_length is not None and content_length > upload_limit:
        payload = {'errors': [error_too_large(upload_limit)]}
        return jsonify(payload), HTTPStatus.REQUEST_ENTITY_TOO_LARGE

    common_single_file()
    return ('', HTTPStatus.NO_CONTENT)


@main.route('/upload-single-restricted-mime-types', methods=['post'])
def upload_single_restricted_mime_types():
    file = common_single_file()

    file_content_type = file.content_type
    allowed_content_types = ['image/jpeg']

    if file_content_type not in allowed_content_types:
        payload = {'errors': [error_wrong_mime_type(allowed_content_types, file_content_type)]}
        return jsonify(payload), HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    return ('', HTTPStatus.NO_CONTENT)
