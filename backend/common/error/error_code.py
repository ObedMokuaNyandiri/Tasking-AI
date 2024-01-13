from enum import Enum
from fastapi import HTTPException


class TKException(Exception):
    pass


class TKHTTPException(TKException):
    pass


class ErrorCode(str, Enum):
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    INCORRECT_PASSWORD = "INCORRECT_PASSWORD"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"
    TOKEN_VALIDATION_FAILED = "TOKEN_VALIDATION_FAILED"
    APIKEY_VALIDATION_FAILED = "APIKEY_VALIDATION_FAILED"
    OBJECT_NOT_FOUND = "OBJECT_NOT_FOUND"
    REQUEST_VALIDATION_ERROR = "REQUEST_VALIDATION_ERROR"
    DATA_MODEL_VALIDATION_ERROR = "DATA_MODEL_VALIDATION_ERROR"
    RESOURCE_LIMIT_REACHED = "RESOURCE_LIMIT_REACHED"
    DUPLICATE_OBJECT = "DUPLICATE_OBJECT"
    ACTION_API_REQUEST_ERROR = "ACTION_API_REQUEST_ERROR"


error_messages = {
    ErrorCode.UNKNOWN_ERROR: {"status_code": 500, "message": "Unknown error occurred."},
    ErrorCode.INTERNAL_SERVER_ERROR: {"status_code": 500, "message": "Internal server error."},
    ErrorCode.INCORRECT_PASSWORD: {"status_code": 401, "message": "Incorrect password."},
    ErrorCode.TOO_MANY_REQUESTS: {"status_code": 429, "message": "Too many requests."},
    ErrorCode.TOKEN_VALIDATION_FAILED: {"status_code": 401, "message": "Token validation failed."},
    ErrorCode.APIKEY_VALIDATION_FAILED: {"status_code": 401, "message": "API key validation failed."},
    ErrorCode.OBJECT_NOT_FOUND: {"status_code": 404, "message": "Object does not exist."},
    ErrorCode.REQUEST_VALIDATION_ERROR: {"status_code": 400, "message": "Request validation error."},
    ErrorCode.DATA_MODEL_VALIDATION_ERROR: {"status_code": 400, "message": "Data model validation error."},
    ErrorCode.RESOURCE_LIMIT_REACHED: {
        "status_code": 429,
        "message": "You have reached the limit of allowed resources.",
    },
    ErrorCode.DUPLICATE_OBJECT: {"status_code": 409, "message": "Duplicate object."},
    ErrorCode.ACTION_API_REQUEST_ERROR: {"status_code": 400, "message": "Action API request error."},
}

assert len(error_messages) == len(ErrorCode)


def raise_http_error(error_code: ErrorCode, message: str):
    raise HTTPException(
        status_code=error_messages[error_code]["status_code"], detail={"error_code": error_code, "message": message}
    )