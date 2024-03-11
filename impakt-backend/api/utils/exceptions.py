from enum import Enum
from typing import Any

from werkzeug.exceptions import HTTPException


class _HTTPExceptionCode(Enum):
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


class AppException(HTTPException):
    def __init__(self, message: str, status_code: _HTTPExceptionCode = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(description=message)

    def __repr__(self):
        return {
            "status_code": self.status_code.value,
            "type": self.status_code.name,
            "message": self.message,
        }

    def __str__(self):
        return self.message


class AppExceptions(Enum):
    BAD_REQUEST = AppException(
        "Resource provided is invalid", _HTTPExceptionCode.BAD_REQUEST
    )
    RESOURCE_NOT_FOUND = AppException(
        "Resource not found", _HTTPExceptionCode.NOT_FOUND
    )
    RESOURCE_EXISTS = AppException(
        "Resource already exists", _HTTPExceptionCode.CONFLICT
    )
    NOT_IMPLEMENTED = AppException(
        "Not implemented", _HTTPExceptionCode.NOT_IMPLEMENTED
    )
    SERVER_ERROR = AppException(
        "Server error", _HTTPExceptionCode.INTERNAL_SERVER_ERROR
    )

    @staticmethod
    def GENERIC_EXCEPTION(message: Any):
        return AppException(str(message), _HTTPExceptionCode.INTERNAL_SERVER_ERROR)
