from typing import Optional
from uuid import UUID, uuid4

from flask import Flask as App


class RequestID(object):
    """
    Flask middleware to ensure all requests have a Request ID header present.

    This ID can be used when logging errors in this application and allows users to trace requests through multiple
    layers such as a load balancer.

    The header value may consist of multiple IDs (see below) but they should be treated as a single, opaque, ID value
    outside of this middleware. Users or their processing tools are responsible for interpreting the Request ID(s).

    To use the Request ID: print(request.environ.get("HTTP_X_REQUEST_ID"))

    The Request ID header is also included in the response back to the client.

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

        Each header value (request ID) is then checked for uniqueness:
        1. if the header is a valid UUID it is considered unique
        2. if the header is from the BAS Load Balancer it is considered unique

        If a unique request ID can't be found, an additional request ID is appended.
        Otherwise the header is returned 'as is'.

        :type header_value: Optional[str]
        :param header_value: value of Request ID HTTP header, may be null
        :rtype: str
        :return: computed value for Request ID HTTP header
        """

        has_unique_header = False

        if header_value is None:
            header_value = self._generate_request_id()
        elif type(header_value) == str:
            header_values = header_value.split(',')
            for request_id in header_values:
                # prevent requiring all header values to be unique
                if not has_unique_header:
                    has_unique_header = self._is_request_id_unique(request_id)

            if not has_unique_header:
                # append a unique header value
                header_value = f"{ header_value },{ self._generate_request_id() }"

        return header_value

    @staticmethod
    def _is_request_id_unique(request_id: str) -> bool:
        """
        Checks whether a Request ID is unique

        Checks:
        1. if a request is from the BAS Load Balancer (which generates unique values)
        2. if a request is a valid UUID

        :type request_id: str
        :param request_id: a Request ID

        :rtype: bool
        :return: whether the Request ID is unique or not
        """

        is_unique = False

        # check if the Request ID is from the BAS Load Balancer
        if 'BAS-API-LB-RV1' in request_id:
            is_unique = True

        # check if the Request ID is a UUID
        try:
            UUID(request_id, version=4)
            is_unique = True
        except ValueError:
            pass

        return is_unique

    @staticmethod
    def _generate_request_id() -> str:
        """
        Generates a unique request ID value

        :rtype: str
        :return: unique request ID
        """

        return str(uuid4())
