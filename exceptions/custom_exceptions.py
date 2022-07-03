from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException


class CustomException(APIException):
    detail_prefix = 'API Service'

    def __init__(self, message=None):
        self.detail = {
            "type": self.detail_prefix + ': ' + self.default_detail,
            "status_code": self.status_code
        }
        if message is not None:
            self.detail["message"] = message


class BadRequest(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad Request'


class Unauthorized(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Unauthorized'


class Forbidden(CustomException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Forbidden'


class NotFound(CustomException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not Found'


class MethodNotAllowed(CustomException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = 'Method not allowed'


class Conflict(CustomException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Conflict with data'


class UnsupportedMediaType(CustomException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    default_detail = 'Unsupported media type'


class ExpectationFailed(CustomException):
    status_code = status.HTTP_417_EXPECTATION_FAILED
    default_detail = 'Unavailable'


class TooManyRequests(CustomException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = 'Too many requests'


class UnprocessableEntityException(CustomException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = 'Unprocessable entity'


class ExceptionFactory:
    @staticmethod
    def create_exception(response, message=None):
        if response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND]:
            return NotFound(message)

        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            return BadRequest(message)

        elif response.status_code == status.HTTP_403_FORBIDDEN:
            return Forbidden(message)

        elif response.status_code == status.HTTP_409_CONFLICT:
            return Conflict(message)

        elif response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE:
            return UnsupportedMediaType(message)

        elif response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            return UnprocessableEntityException(message)

        elif response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            return TooManyRequests(message)

        else:
            return ExpectationFailed(message)
