import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from extensions.fastapi.api import failed_response, validation_error_response

logger = logging.getLogger('exception_handler')


class APIException(Exception):
    """api 异常
    """
    error_type = 'api_error'
    error_message = 'A server error occurred.'

    def __init__(self, error_type=None, error_message=None):
        if error_type is not None:
            self.error_type = error_type
        if error_message is not None:
            self.error_message = error_message

    def __repr__(self):
        return '<{} {}: {}>'.format(
            self.__class__, self.error_type, self.error_message
        )


class GlobalExceptionHandler:

    def __init__(self, app: FastAPI):
        self.app = app

    @staticmethod
    async def handle_request_validation_error(
        request: Request, error: RequestValidationError
    ):
        return validation_error_response(error)

    @staticmethod
    async def handle_api_exception(request: Request, error: APIException):
        return failed_response(
            error_type=error.error_type, error_message=error.error_message
        )

    @staticmethod
    async def handle_exception(request: Request, error: Exception):
        logger.error(f'{request.url} {error}')
        return failed_response(
            error_type='server_error', error_message='Server error'
        )

    def init(self):
        self.app.add_exception_handler(
            RequestValidationError, self.handle_request_validation_error
        )
        self.app.add_exception_handler(APIException, self.handle_api_exception)
        self.app.add_exception_handler(Exception, self.handle_exception)


class PermissionDenied(APIException):
    error_type = 'permission_denied'
    error_message = 'Permission denied'


class ObjectNotFound(APIException):
    error_type = 'object_not_found'
    error_message = 'Object not found'
