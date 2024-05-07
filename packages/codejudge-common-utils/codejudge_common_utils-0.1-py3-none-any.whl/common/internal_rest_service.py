import log_request_id

from codejudgework.settings import *
from restapi.common.common_rest_util import CommonRestUtil, CallType

logger = logging.getLogger(__name__)


class InternalRestService:

    @staticmethod
    def execute(request, url, data, method, headers, via_auth_token, multipart_request=False):
        headers = InternalRestService.validate_and_prepare_headers(headers, request, url, method, via_auth_token)
        r = CommonRestUtil.execute(url, data, method, headers, CallType.INTERNAL, multipart_request)
        return r.json()

    @staticmethod
    def validate_and_prepare_headers(headers, request, url, method, via_auth_token):
        if not url:
            raise Exception("Url can't be empty!")
        if not method:
            raise Exception("Method can't be empty!")
        if via_auth_token is None:
            raise Exception("Via Auth Token Boolean flag can't be empty")

        if not headers:
            headers = {}
        headers['content-type'] = 'application/json'
        headers['accept'] = 'application/json'
        headers[REQUEST_UUID_KEY] = getattr(log_request_id.local, 'request_id', None)

        if via_auth_token is True or request:
            if via_auth_token is True:
                headers['auth-token'] = AUTH_TOKEN
            if request:
                headers['cj-header'] = request.META.get('HTTP_CJ_HEADER')
                headers['ent-header'] = CommonRestUtil.get_request_ent_header(request)
                headers['Authorization'] = CommonRestUtil.get_request_authorization_header(request)
        else:
            raise Exception("Request can't be empty!")
        return headers
