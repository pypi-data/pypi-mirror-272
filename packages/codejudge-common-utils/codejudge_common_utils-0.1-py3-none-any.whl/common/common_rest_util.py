import json
import logging
import re
from enum import Enum

import requests
from requests import Request, Session

from restapi.common.json_util import JsonUtil
from restapi.common.map_util import MapUtil
from restapi.common.validators import Validator
from restapi.exception.exception import RecruitException

logger = logging.getLogger(__name__)


class RestMethod(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4
    PATCH = 5

    @classmethod
    def get_rest_method(cls, method_str):
        for member in RestMethod:
            if method_str == member.name:
                return member
        return None


class CallType(Enum):
    INTERNAL = 1
    EXTERNAL = 2


class CommonRestUtil:

    @staticmethod
    def execute(url, data, method, headers, type, multipart_request=False, form_data=False, timeout_seconds=None):
        r = None
        if method is RestMethod.GET:
            r = requests.get(url=url, params=data, headers=headers, timeout=timeout_seconds)
        elif method is RestMethod.POST:
            if form_data:
                files = CommonRestUtil.get_data_from_dict(data)
                request = Request(method=method.name, url=url, files=files, headers=headers).prepare()
                r = Session().send(request, timeout=timeout_seconds)
            else:
                r = requests.post(url=url, json=data, headers=headers, timeout=timeout_seconds)
        elif method is RestMethod.PUT:
            if form_data:
                files = CommonRestUtil.get_data_from_dict(data)
                request = Request(method=method.name, url=url, files=files, headers=headers).prepare()
                r = Session().send(request, timeout=timeout_seconds)
            else:
                r = requests.put(url=url, json=data, headers=headers, timeout=timeout_seconds)
        elif method is RestMethod.DELETE:
            r = requests.delete(url=url, params=data, headers=headers, timeout=timeout_seconds)
        elif method is RestMethod.PATCH:
            r = requests.patch(url=url, params=data, headers=headers, timeout=timeout_seconds)

        if r and r.status_code in (200, 201, 202):
            return r
        else:
            raise RecruitException(message=CommonRestUtil.__get_exception_msg(r, type), status=r.status_code)


    @staticmethod
    def read_json_data_from_url(url):
        response = requests.get(url)
        if response.status_code == 200:
            json_data = json.loads(response.content)
            return json_data
        else:
            return None

    @staticmethod
    def get_data_from_dict(data):
        if not MapUtil.is_valid(data):
            return None
        files = {}
        for key, value in data.items():
            files[key] = (None, JsonUtil.convert_dict_to_json(value))
        return files

    @staticmethod
    def get_request_id(request):
        if hasattr(request, 'id'):
            return request.id
        return None

    @staticmethod
    def get_request_method(request):
        return request.META.get('REQUEST_METHOD')

    @staticmethod
    def get_request_uri(request):
        final_uri = ''
        uri = request.META.get('PATH_INFO')
        if uri:
            uri_split = uri.split('/')
            for split in uri_split:
                if split:
                    if split.isnumeric() is False:
                        final_uri += '/' + split
        return final_uri + '/'

    @staticmethod
    def get_request_accept(request):
        return request.META.get('HTTP_ACCEPT')

    @staticmethod
    def get_request_ent_header(request):
        return request.META.get('HTTP_ENT_HEADER')

    @staticmethod
    def get_request_authorization_header(request):
        return request.META.get('HTTP_AUTHORIZATION')

    @staticmethod
    def get_client_info(request):
        return request.META.get('HTTP_CLIENT_INFO')

    @staticmethod
    def get_request_url(request):
        return request.build_absolute_uri('?')

    @staticmethod
    def get_request_params(request):
        return request.build_absolute_uri().replace(request.build_absolute_uri('?'), '')

    @staticmethod
    def get_request_headers_json(request):
        headers = CommonRestUtil.get_request_headers(request)
        return json.dumps(headers)

    @staticmethod
    def get_request_headers(request):
        regex = re.compile('^HTTP_')
        headers = dict((regex.sub('', header), value) for (header, value)
                       in request.META.items() if header.startswith('HTTP_'))
        return headers

    @staticmethod
    def get_request_timezone(request):
        request_headers = CommonRestUtil.get_request_headers(request)
        return request_headers.get('TIMEZONE', 'Asia/Kolkata')

    @staticmethod
    def __get_exception_msg(r, call_type):
        error_message = r.text
        status_code = r.status_code

        if call_type == CallType.INTERNAL:
            if Validator.is_json_string_valid(error_message):
                error_response = r.json()
                if error_response:
                    if 'message' in error_response:
                        error_message = error_response['message']
                    elif 'msg' in error_message:
                        error_message = error_response['msg']

        logger.error(str(call_type) + 'Service Call failed because: ' + error_message + ' with status code: '
                     + str(status_code))

        return error_message
