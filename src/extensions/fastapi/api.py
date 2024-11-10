import functools
import inspect
from typing import Any, Callable, Generic, List, TypeVar

from fastapi import APIRouter
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic.generics import GenericModel
from starlette.responses import Response

T = TypeVar('T')


class APIResponse(GenericModel, Generic[T]):
    success: bool
    msg: str
    data: T = None


def success_response(data=''):
    """successful response
    """
    new_body = {'success': True, 'msg': '', 'data': data}
    return new_body


def failed_response(error_type, error_message, error_data=None):
    """failed response
    """
    new_body = {
        'success': False,
        'error_type': error_type,
        'msg': error_message,
        'data': ''
    }
    if error_data is not None:
        new_body['data'] = error_data
    return JSONResponse(new_body)


def validation_error_response(validation_error: RequestValidationError):
    """字段验证失败的 response
    validation_error: ValidationError
    """
    errors = list()

    for error in validation_error.raw_errors:
        if not hasattr(error.exc, 'raw_errors'):
            continue

        for raw_error in error.exc.raw_errors:
            field_error = {
                'error_type': 'validation_error',
                'error': raw_error._loc,
                'msg': str(raw_error.exc)
            }
            errors.append(field_error)

    new_body = {
        'success': False,
        'error_type': 'data_validation_errors',
        'msg': 'Data has validation errors',
        'data': errors
    }
    return JSONResponse(new_body)


def route(
    router: APIRouter,
    path: str,
    methods: List[str],
    response_model=None,
    **options
):
    common_response_model = APIResponse[response_model]

    def wrapper(func: Callable[..., Any]):

        async def decorator(*args, **kwargs):
            response = await func(*args, **kwargs)
            if isinstance(response, Response):
                # The response may have already been wrapped, this situation should be ignored.
                return response

            return success_response(response)

        signature = inspect.signature(func)
        decorator.__signature__ = signature
        decorator.__name__ = func.__name__
        decorator.__doc__ = func.__doc__
        router.add_api_route(
            path,
            endpoint=decorator,
            response_model=common_response_model,
            methods=methods,
            **options
        )
        return decorator

    return wrapper


get = functools.partial(route, methods=['GET'])
post = functools.partial(route, methods=['POST'])
put = functools.partial(route, methods=['PUT'])
delete = functools.partial(route, methods=['DELETE'])
