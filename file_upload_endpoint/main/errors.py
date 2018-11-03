from http import HTTPStatus
from uuid import uuid4

import sentry_sdk
from flask import current_app as app


def error_no_file(field: str) -> dict:
    """
    Creates an error for a missing file input in a request

    TODO: Refactor to use validation error [#35]

    :type field: str
    :param field: Name of the missing file input

    :rtype: dict
    :return Complete JSON-API compatible error object
    """
    log_message = f"[{ field }] field missing in request"
    app.logger.warning(log_message)

    # As the API handles this error through this error message, it is not reported to Sentry.
    # However, because it's useful for tracking, we want report it anyway.
    with sentry_sdk.push_scope() as scope:
        scope.set_extra('debug', False)
        sentry_sdk.capture_message(log_message)

    return {
        'id': uuid4(),
        'status': HTTPStatus.BAD_REQUEST,
        'title': f"[{ field }] field missing in request",
        'detail': 'Check the name of the field and that the request uses multipart/form-data encoding'
    }


def error_no_file_selection(field: str) -> dict:
    """
    Creates an error for an empty file input in a request

    TODO: Refactor to use validation error [#35]

    :type field: str
    :param field: Name of the missing file input

    :rtype: dict
    :return Complete JSON-API compatible error object
    """
    log_message = f"[{ field }] field value is an empty selection"
    app.logger.warning(log_message)

    # As the API handles this error through this error message, it is not reported to Sentry.
    # However, because it's useful for tracking, we want report it anyway.
    with sentry_sdk.push_scope() as scope:
        scope.set_extra('debug', False)
        sentry_sdk.capture_message(log_message)

    return {
        'id': uuid4(),
        'status': HTTPStatus.BAD_REQUEST,
        'title': f"[{ field }] field value is an empty selection",
        'detail': 'Check the file selected is specified correctly and is a valid file'
    }


def error_wrong_mime_type(valid_mime_types: list, invalid_mime_type: str) -> dict:
    """
    Creates an error for an file input in a request that uses an unsupported MIME type

    TODO: Refactor to use validation error [#35]

    :type valid_mime_types: str
    :param valid_mime_types: List of valid MIME types

    :type invalid_mime_type: str
    :param invalid_mime_type: Mime type used that is not in the list of valid types

    :rtype: dict
    :return Complete JSON-API compatible error object
    """
    log_message = f"File type uploaded, [{ invalid_mime_type }], is not allowed"
    app.logger.warning(log_message)

    # As the API handles this error through this error message, it is not reported to Sentry.
    # However, because it's useful for tracking, we want report it anyway.
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
