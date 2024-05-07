from codejudgework.settings import *
from restapi.common.common_rest_util import CommonRestUtil, CallType

logger = logging.getLogger(__name__)


class ExternalRestService:

    @staticmethod
    def execute(url, data, method, headers, multipart_request=False, form_data=False, timeout_seconds=None):
        headers = ExternalRestService.validate_and_prepare_headers(headers, url, method)
        return CommonRestUtil.execute(url, data, method, headers, CallType.EXTERNAL, multipart_request, form_data, timeout_seconds)

    @staticmethod
    def validate_and_prepare_headers(headers, url, method):
        if not url:
            raise Exception("Url can't be empty!")
        if not method:
            raise Exception("Method can't be empty!")

        if not headers:
            headers = {}

        return headers

    @staticmethod
    def read_data_from_external_url(url):
        return CommonRestUtil.read_json_data_from_url(url)

