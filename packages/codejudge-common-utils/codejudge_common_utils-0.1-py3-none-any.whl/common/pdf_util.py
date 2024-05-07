import json
import os

import jinja2
import pdfkit

from codejudgework.settings import WKTHTMLTOPDF_PATH, SEJDA_URL, SEJDA_API_KEY, USE_PDF_EXTERNAL_SERVICE
from restapi.common.external_rest_service import ExternalRestService
from restapi.common.common_rest_util import RestMethod


class PDFUtil:

    @staticmethod
    def render_and_convert_html_to_pdf(tpl_path, context, out_file_name, page_options={}):
        rendered_html = PDFUtil.render(tpl_path, context)
        return PDFUtil.convert_html_to_pdf(rendered_html, out_file_name, page_options)

    @staticmethod
    def render(tpl_path, context):
        path, filename = os.path.split(tpl_path)
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(path or './')
        ).get_template(filename).render(context)

    @staticmethod
    def convert_html_to_pdf(in_file_content, out_filename, page_options={}):
        if USE_PDF_EXTERNAL_SERVICE:
            return PDFUtil.__convert_html_to_pdf_external(in_file_content, out_filename, page_options)

        options = {}
        # os.environ['DISPLAY'] = ':0'
        config = pdfkit.configuration(wkhtmltopdf=WKTHTMLTOPDF_PATH)
        return pdfkit.from_string(in_file_content, out_filename, options=options, configuration=config)

    @staticmethod
    def __convert_html_to_pdf_external(in_file_content, out_filename, page_options={}):
        url = SEJDA_URL
        data = {
            'htmlCode': in_file_content,
            'pageSize': 'a4' if 'page_size' not in page_options else page_options['page_size'],
            # 'pageMargin': 1 if 'page_margin' not in page_options else page_options['page_margin'],
            'pageMargin': 0 if 'page_margin' not in page_options else page_options['page_margin'],
            'pageOrientation': 'portrait',
            'usePrintMedia': 'true',
            'pageMarginUnits': 'cm'
        }
        if 'page_viewport_width' in page_options:
            data['viewportWidth'] = page_options['page_viewport_width']
        method = RestMethod.POST
        headers = {
            'Authorization': 'Token: {}'.format(SEJDA_API_KEY)
        }
        r = ExternalRestService.execute(url, data, method, headers, multipart_request=True)
        open(out_filename, 'wb').write(r.content)

    @classmethod
    def generate_pdf_from_html(cls, request):
        pass
