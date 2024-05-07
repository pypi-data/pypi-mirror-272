import re
import logging

from rest_framework import status

from restapi.common.validators import Validator
from restapi.exception.exception import RecruitException

logger = logging.getLogger(__name__)

ALPHA_NUM_SYMBOLS_REGEX = "^[ A-Za-z0-9_@.'’/#&+,?<>=!()-]*$"
ALL_NON_ALPHA_NUM_SYMBOLS_REGEX_CHAR_REPLACE = "[^\\sA-Za-z0-9_@.'’/#&+,?<>=!()-]+"
ATS_TEST_ID_TAG_REGEX = r"CJ-[0-9]+"
KEY_VALUE_REGEX = r"\('([^']+)', '([^']+)'\)"
NUM_SYMBOL_REGEX = r"[0-9!@#$%^&*()_+{}[\]:;<>,.?~\\/-]"
NUM_REGEX = r"\d"
ALPHA_AND_UNDERSCORE = "^[a-zA-Z_ ]+$"


class StrRegex:

    @classmethod
    def validate_str_for_alpha_num_symbol(cls, string):
        is_valid = Validator.is_valid_string(string)
        if is_valid:
            match = re.search(ALPHA_NUM_SYMBOLS_REGEX, string)
            return True if match else False

    @classmethod
    def transform_and_validate_str_for_alpha_num_symbol(cls, string):
        is_valid = cls.validate_str_for_alpha_num_symbol(string)
        if not is_valid:
            transformed_str = re.sub(ALL_NON_ALPHA_NUM_SYMBOLS_REGEX_CHAR_REPLACE, ' ', string)
            return re.sub(' +', ' ', transformed_str)
        return re.sub(' +', ' ', string)

    @classmethod
    def validate_ats_tag_test_id(cls, string):
        pattern = re.compile(ATS_TEST_ID_TAG_REGEX, re.IGNORECASE)
        return pattern.match(string)

    @classmethod
    #TODO: to handle very old cases
    def validate_regex_for_job_role(cls, string):
        is_valid = Validator.is_valid_string(string)
        if is_valid:
            match = re.search(ALPHA_AND_UNDERSCORE, string)
            return True if match else False
        return False

    @classmethod
    def validate_candidate_name(cls, string):
        Validator.validate_string(string, 'Name')
        if re.search(NUM_SYMBOL_REGEX, string):
            raise RecruitException(message="Name should not contain numbers or special characters!",
                                   status=status.HTTP_400_BAD_REQUEST)
