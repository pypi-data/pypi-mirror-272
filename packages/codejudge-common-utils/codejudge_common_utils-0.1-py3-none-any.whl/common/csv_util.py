import csv
import io
import logging
import sys

from django.utils.encoding import smart_str
from pytz import unicode

from restapi.common.json_util import JsonUtil
from restapi.common.list_util import ListUtil
from restapi.common.string_util import StringUtil
from restapi.exception.util import ExceptionUtil

logger = logging.getLogger(__name__)


class CSVUtil:

    @staticmethod
    def write_to_csv(file_name, headers, values):
        with open(file_name, 'w+') as output_file:
            dict_writer = csv.DictWriter(output_file, headers)
            dict_writer.writeheader()
            if ListUtil.is_valid(values):
                for value in values:
                    for key in value:
                        value[key] = unicode(value[key]).encode("utf-8")
                        value[key] = value[key].decode('utf-8', errors='ignore')
                    try:
                        dict_writer.writerow(value)
                    except Exception as ex:
                        error_msg = 'Error occured while exporting the report for the row with error: {}'.format(ex)
                        logger.error(error_msg, ex)


                        ExceptionUtil.send_exception_mail_worker_v2(JsonUtil.convert_dict_to_json(dict(value=value,
                                                                                                error_msg=error_msg)),
                                                                    file_name,
                                                                    ex)

                        pass
            # dict_writer.writerows(values)


    @staticmethod
    def read_from_csv(file_from_request):
        logger.info('got request to read data from csv of filename -> {}'.format(file_from_request))
        response = []
        file = file_from_request.read().decode('utf-8')
        csvreader = csv.DictReader(io.StringIO(file))
        for row in csvreader:
            response.append(row)
        return response
