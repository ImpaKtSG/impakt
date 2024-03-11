from typing import Any
from flask import jsonify


class _HTTPExceptionCode:
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    PAYLOAD_TOO_LARGE = 413
    URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    IM_A_TEAPOT = 418
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505


class AppException(Exception):
    """Custom exception class for the application.

    This class extends the built-in Exception class and adds a type and status code.

    Args:
        type (str): The type of the exception.
        status_code (_HTTPExceptionCode, optional): The HTTP status code associated with the exception. Defaults to 400.
        message (str, optional): The error message. Defaults to None.

    Attributes:
        type (str): The type of the exception.
        message (str): The error message.
        status_code (_HTTPExceptionCode): The HTTP status code associated with the exception.
    """

    def __init__(
        self, type: str, status_code: _HTTPExceptionCode = 400, message: str = None
    ):
        self.type = type
        self.message = message
        self.status_code = status_code
        super().__init__(message)

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "type": self.type,
            "message": self.message,
        }

    def __repr__(self):
        return jsonify(self.to_dict())

    def __str__(self):
        return self.message


class AppExceptions:
    BAD_REQUEST = AppException(
        "BAD_REQUEST", _HTTPExceptionCode.BAD_REQUEST, "Resource provided is invalid"
    )
    RESOURCE_NOT_FOUND = AppException(
        "RESOURCE_NOT_FOUND", _HTTPExceptionCode.NOT_FOUND, "Resource not found"
    )
    RESOURCE_EXISTS = AppException(
        "RESOURCE_EXISTS", _HTTPExceptionCode.CONFLICT, "Resource already exists"
    )
    NOT_IMPLEMENTED = AppException(
        "NOT_IMPLEMENTED", _HTTPExceptionCode.NOT_IMPLEMENTED, "Not implemented"
    )
    SERVER_ERROR = AppException(
        "SERVER_ERROR", _HTTPExceptionCode.INTERNAL_SERVER_ERROR, "Server error"
    )

    @staticmethod
    def GENERIC_EXCEPTION(message: Any):
        return AppException(
            "GENERIC_EXCEPTION", _HTTPExceptionCode.INTERNAL_SERVER_ERROR, str(message)
        )
