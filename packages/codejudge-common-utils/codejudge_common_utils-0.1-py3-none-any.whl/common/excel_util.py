import logging
import pandas as pd
from pytz import unicode
from tablepyxl import tablepyxl
from restapi.common.json_util import JsonUtil
from restapi.common.list_util import ListUtil
from restapi.common.map_util import MapUtil
from restapi.exception.util import ExceptionUtil

logger = logging.getLogger(__name__)

class ExcelUtil:

    @staticmethod
    def write_to_excel_using_table_pyxl(file_name, headers, values):
        if ListUtil.is_valid(headers) and ListUtil.is_valid(values):
            column_name_to_type_map = {}
            table_tag = "<table>"
            headers_internal_html = ""
            body_internal_html = ""
            single_candidate = values[0]
            for header in headers:
                ExcelUtil.__decorate_value(header, single_candidate)
                headers_internal_html += "<th>" + str(header) + "</th>"
                column_name_to_type_map[header] = type(single_candidate[header])
            headers_final_html = "<thead> <tr>" + headers_internal_html + "</tr> </thead>"
            for value in values:
                body_per_candidate_html = ""
                for header in headers:
                    ExcelUtil.__decorate_value(header, value)
                    body_per_candidate_html += "<td style=\"white-space:pre;\" class=\"{}\">".format(ExcelUtil.__get_table_pyxl_td_class_type_based_on_column_type(column_name_to_type_map[header])) + str(value[header]) + "</td>"
                body_internal_html += "<tr>" + body_per_candidate_html + "</tr>"
            body_final_html = "<tbody>" + body_internal_html + "</tbody>"
            table = table_tag + headers_final_html + body_final_html
            try:
                return tablepyxl.document_to_xl(table, file_name)
            except Exception as ex:
                error_msg = 'Error occurred while exporting the report with error: {}'.format(ex)
                logger.error(error_msg, ex)
                ExceptionUtil.send_exception_mail_worker_v2(JsonUtil.convert_dict_to_json(dict(error_msg=error_msg)), file_name, ex)
                pass

    @staticmethod
    def __decorate_value(header, value):
        if MapUtil.check_if_map_has_key(value, header) and value[header] is not None:
            value[header] = unicode(value[header]).encode("utf-8")
            value[header] = value[header].decode('utf-8', errors='ignore')
        else:
            value[header] = "-"

    @staticmethod
    def __get_table_pyxl_td_class_type_based_on_column_type(column_type):
        column_type_to_td_class_internal_map = {
            type("a"): "TYPE_STRING",
            type(1): "TYPE_INTEGER",
            type(True): "TYPE_BOOL",
            type(None): "TYPE_NULL",
            type(1.1): "TYPE_NUMERIC"
        }
        return column_type_to_td_class_internal_map.get(column_type) if column_type in column_type_to_td_class_internal_map else "TYPE_STRING"

