"""
utils for generating api responses
"""
import json
import re
from enum import Enum, unique

from django.db import models
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods


@unique
class ErrorCode(Enum):
    """
    api error code enumeration
    """

    # success code family
    SUCCESS = 200  # deprecated
    SUCCESS_CODE = 200_00

    # bad request family
    INVALID_REQUEST_ARGS = 400  # deprecated
    BAD_REQUEST_ERROR = 400_00
    INVALID_REQUEST_ARGUMENT_ERROR = 400_01
    REQUIRED_ARG_IS_NULL_ERROR = 400_02

    # unauthorized family
    UNAUTHORIZED = 401  # deprecated
    UNAUTHORIZED_ERROR = 401_00

    # refuse family
    REFUSE_ACCESS = 403  # deprecated
    REFUSE_ACCESS_ERROR = 403_00
    CONFIRM_CHECK_OUT = 403_01
    SEAT_ARRANGEMENT_ERROR = 403_02

    # not found family
    ITEM_NOT_FOUND = 404  # deprecated
    NOT_FOUND_ERROR = 404_00

    # duplicated family
    ITEM_ALREADY_EXISTS = 409  # deprecated
    DUPLICATED_ERROR = 409_00


class SetType(Enum):
    """
    the argument named type for PUT
    if not in these, the int mean the id of model
    """
    SET_NONE = -1
    NONE = 0


def _api_response(success, data) -> dict:
    """
    wrap an api response dict obj
    :param success: whether the request is handled successfully
    :param data: requested data
    :return: a dictionary object, like {'success': success, 'data': data}
    """
    return {'success': success, 'data': data}


def failed_api_response(code, error_msg=None) -> dict:
    """
    wrap an failed response dict obj
    :param code: error code, refers to ErrorCode, can be an integer or a str (error name)
    :param error_msg: external error information
    :return: an api response dictionary
    """
    if isinstance(code, str):
        code = ErrorCode[code]
    if isinstance(code, int):
        code = ErrorCode(code)
    assert isinstance(code, ErrorCode)
    assert isinstance(code.value, int)

    if code.value < 1000:
        # using simple http status code is deprecated
        import warnings
        warnings.warn("using simple http code {} is deprecated".format(code.name))
        code = ErrorCode(code.value * 100)  # set to new style error code

    assert code.value >= 10000

    if error_msg is None:
        error_msg = str(code)
    # else:
    #     error_msg = str(code) + ': ' + error_msg

    status_code = code.value // 100
    detailed_code = code.value
    return _api_response(
        success=False,
        data={
            'code': status_code,
            'detailed_error_code': detailed_code,
            'error_msg': error_msg
        })


def success_api_response(data) -> dict:
    """
    wrap a success response dict obj
    :param data: requested data
    :return: an api response dictionary
    """
    return _api_response(True, data)


def response_wrapper(func):
    """
    decorate a given api-function, parse its return value from a dict to a HttpResponse
    :param func: a api-function
    :return: wrapped function
    """

    def _inner(*args, **kwargs):
        _response = func(*args, **kwargs)
        if isinstance(_response, dict):
            if _response['success']:
                _response = JsonResponse(_response['data'])
            else:
                status_code = _response.get("data").get("code")
                _response = JsonResponse(_response['data'])
                _response.status_code = status_code
        _response['Access-Control-Allow-Origin'] = '*'
        return _response

    return _inner


def wrapped_api(api_dict: dict):
    """
    wrap apis together with 4 methods(get/post/put/delete)
    :param api_dict: dict as {'get': get_api, 'post': post_api ...}
    :return: a api
    """
    assert isinstance(api_dict, dict)
    api_dict = {k.upper(): v for k, v in api_dict.items()}
    assert set(api_dict.keys()).issubset(['GET', 'POST', 'PUT', 'DELETE'])

    @require_http_methods(api_dict.keys())
    def _api(request, *args, **kwargs):
        return api_dict[request.method](request, *args, **kwargs)

    return _api


def parse_data(request: HttpRequest):
    """Parse request body and generate python dict

    Args:
        request (HttpRequest): all http request

    Returns:
        | request body is malformed = None
        | otherwise                 = python dict
    """
    try:
        return json.loads(request.body.decode())
    except json.JSONDecodeError:
        return None
