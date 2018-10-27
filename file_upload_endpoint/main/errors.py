from http import HTTPStatus
from uuid import uuid4

import sentry_sdk
from flask import current_app as app


def error_no_file(field):
    log_message = f"[{ field }] field missing in request"
    app.logger.warning(log_message)

    # as the API handles this error with this error message it is not reported to Sentry
    # however, because it's useful for tracking, an event is sent anyway.
    with sentry_sdk.push_scope() as scope:
        scope.set_extra('debug', False)
        sentry_sdk.capture_message(log_message)

    return {
        'id': uuid4(),
        'status': HTTPStatus.BAD_REQUEST,
        'title': f"[{ field }] field missing in request",
        'detail': 'Check the name of the field and that the request uses multipart/form-data encoding'
    }


def error_no_file_selection(field):
    log_message = f"[{ field }] field value is an empty selection"
    app.logger.warning(log_message)

    # as the API handles this error with this error message it is not reported to Sentry
    # however, because it's useful for tracking, an event is sent anyway.
    with sentry_sdk.push_scope() as scope:
        scope.set_extra('debug', False)
        sentry_sdk.capture_message(log_message)

    return {
        'id': uuid4(),
        'status': HTTPStatus.BAD_REQUEST,
        'title': f"[{ field }] field value is an empty selection",
        'detail': 'Check the file selected is specified correctly and is a valid file'
    }


def error_wrong_mime_type(valid_mime_types, invalid_mime_type):
    log_message = f"File type uploaded, [{ invalid_mime_type }], is not allowed"
    app.logger.warning(log_message)

    # as the API handles this error with this error message it is not reported to Sentry
    # however, because it's useful for tracking, an event is sent anyway.
    with sentry_sdk.push_scope() as scope:
        scope.set_extra('debug', False)
        sentry_sdk.capture_message(log_message)

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
