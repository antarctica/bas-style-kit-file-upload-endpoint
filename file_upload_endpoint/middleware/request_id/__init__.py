import uuid
from typing import Optional

from flask import Flask as App


class RequestID(object):
    """
    Flask middleware to ensure all requests have a request ID header present.

    This ID can be used when logging errors in this application and allows users to trace requests through multiple
    layers such as a load balancer.

    The header value may consist of multiple IDs (see below) but they should be treated as a single, opaque, ID value
    outside of this middleware. Users or their processing tools are responsible for interpreting the request ID(s).

    To use the request ID: print(request.environ.get("HTTP_X_REQUEST_ID"))

    Where possible we try to ensure there is at least one unique request ID value (typically a UUID) whilst respecting
    a request ID value given by a client, but which may not be unique.
    """
    def __init__(self, app: App):
        self._header_name = "X-Request-ID"
        self._flask_header_name = f"HTTP_{ self._header_name.upper().replace('-', '_') }"
        self.app = app.wsgi_app
        app.wsgi_app = self

    def __call__(self, environ, start_response) -> App:
        request_id_header = self._compute_request_id_header(environ.get(self._flask_header_name))
        environ[self._flask_header_name] = request_id_header

        def new_start_response(status, response_headers, exc_info=None):
            response_headers.append((self._header_name, request_id_header))
            return start_response(status, response_headers, exc_info)

        return self.app(environ, new_start_response)

    def _compute_request_id_header(self, header_value: Optional[str] = None) -> str:
        """
        Computes a request ID header based on a possibly existing value

        If there isn't an existing header, a single unique request ID is generated and returned.

        If there is an existing header, it is split to check for multiple values as per RFC 2616.
        If there is a single header value, an additional request ID is appended and both returned.
        If there are multiple header values, the header is returned 'as-is'.

        :type header_value: Optional[str]
        :param header_value: value of request ID HTTP header, may be null
        :rtype: str
        :return: computed, complete, value for request ID HTTP header
        """
        if header_value is None:
            header_value = self._generate_request_id()
        elif type(header_value) == str:
            if len(header_value.split(',')) == 1:
                header_value = f"{ header_value.strip() },{ self._generate_request_id() }"

        return header_value

    @staticmethod
    def _generate_request_id() -> str:
        """
        Generates a unique request ID value

        :rtype: str
        :return: unique request ID
        """
        return str(uuid.uuid4())
