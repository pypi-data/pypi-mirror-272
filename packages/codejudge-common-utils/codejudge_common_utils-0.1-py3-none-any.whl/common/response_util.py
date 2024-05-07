import logging

from django.http import HttpResponse

logger = logging.getLogger(__name__)


class ResponseUtil:

    @staticmethod
    def return_file_response(file, content_type, filename='results.pdf'):
        logger.info("got request to return file response...")
        http_response = HttpResponse(file['Body'].read(), content_type=content_type)
        http_response['Content-Disposition'] = "attachment;filename=" + filename
        return http_response
