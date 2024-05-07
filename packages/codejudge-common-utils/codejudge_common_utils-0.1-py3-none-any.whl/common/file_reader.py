from enum import Enum

from tablib import Dataset

from restapi.common.file_util import FileUtil
from restapi.common.transformers import Transformers
from restapi.common.validators import Validator


class FileType(Enum):
    SPREAD_SHEET = 'spread_sheet'


file_type_to_attributes_mapping = dict()
file_type_to_attributes_mapping[FileType.SPREAD_SHEET] = dict()
file_type_to_attributes_mapping[FileType.SPREAD_SHEET]['types'] = ['vnd.ms-excel', 'csv', 'octet-stream',
                                                                  'vnd.openxmlformats-officedocument.spreadsheetml.sheet']
file_type_to_attributes_mapping[FileType.SPREAD_SHEET]['error_msg'] = 'Only xls/csv/xlsx file type is supported!'


class FileReader:

    @classmethod
    def read_file_date(cls, file, file_type_enum):
        data_set = Dataset()
        file_type = Validator.validate_and_get_file_type(file,
                                                         file_type_to_attributes_mapping[file_type_enum]['types'],
                                                         file_type_to_attributes_mapping[file_type_enum]['error_msg'])
        file_content = FileUtil.get_file_content(file, file_type)
        data = data_set.load(file_content)
        imported_list_of_dict = data.dict
        return cls.__get_transformed_list_of_dict(imported_list_of_dict)

    @classmethod
    def __get_transformed_list_of_dict(cls, imported_dict):
        transformed_list_of_dict = []
        if imported_dict:
            for item in imported_dict:
                transformed_dict = dict()
                for key in item:
                    transformed_key = Transformers.to_lower_case_and_trim(key)
                    transformed_dict[transformed_key] = item[key]
                transformed_list_of_dict.append(transformed_dict)
        return transformed_list_of_dict
