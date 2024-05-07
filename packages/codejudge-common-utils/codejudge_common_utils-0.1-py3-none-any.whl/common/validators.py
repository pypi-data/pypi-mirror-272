import inspect
import json
import logging
import numbers
import re
from builtins import type
from datetime import datetime
from logging import Logger

import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from pyisemail import is_email
from django.utils import timezone
from rest_framework import status

from codejudgework.settings import MAX_FILE_UPLOAD_SIZE, MAX_FILE_UPLOAD_SIZE_STR
from restapi.common.file_util import FileUtil
from restapi.common.map_util import MapUtil
from restapi.common.transformers import Transformers
from restapi.exception.exception import RecruitException


logger = logging.getLogger(__name__)


class Validator:

    @classmethod
    def validate_empty_arr(cls, arr, entity_name):
        if arr is None or len(arr) == 0:
            raise RecruitException(message=entity_name + " can't be empty!", status=status.HTTP_400_BAD_REQUEST)
        return arr

    @classmethod
    def is_valid_string(cls, string):
        return False if string in [None, ''] else True

    @classmethod
    def validate_string(cls, string, entity_name=None, error_msg=None):
        cls.__validate_validation_params(entity_name, error_msg)

        if not Validator.is_valid_string(string):
            cls.__throw_exception(entity_name, error_msg)

    @classmethod
    def is_json_string_valid(cls, json_str):
        if json_str:
            try:
                json_obj = json.loads(json_str)
                return True
            except ValueError as e:
                return False
        return False

    @classmethod
    def validate_string_with_len(cls, input_string, length, entity_name_for_invalid_string=None,
                                 error_msg_for_invalid_string=None, entity_name_for_len_error=None,
                                 error_msg_for_len_error=None):
        cls.validate_string(input_string, entity_name_for_invalid_string, error_msg_for_invalid_string)
        cls.__validate_validation_params(entity_name_for_len_error, error_msg_for_len_error)
        if len(input_string) > length:
            error_str=None
            if error_msg_for_len_error is None:
                error_str = entity_name_for_len_error + " must be less than or equal to " + str(length) + " characters!"
            else:
                error_str = error_msg_for_len_error
            raise RecruitException(message=error_str, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_number(cls, number, entity_name=None, error_msg=None):
        cls.__validate_validation_params(entity_name, error_msg)

        if number in [None]:
            cls.__throw_exception(entity_name, error_msg)

    @classmethod
    def validate_number_gt_than(cls, number, min_value, entity_name=None, error_msg=None):
        cls.validate_number(number, entity_name, error_msg)
        if isinstance(number, numbers.Number) is False:
            cls.__throw_exception(entity_name, '{} must be a number!'.format(entity_name))
        if number <= min_value:
            if error_msg:
                raise RecruitException(message=error_msg, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise RecruitException(message='{} must be greater than {}!'.format(entity_name, min_value), status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_number_lt_than(cls, number, max_value, entity_name=None, error_msg=None):
        cls.validate_number(number, entity_name, error_msg)
        if isinstance(number, numbers.Number) is False:
            cls.__throw_exception(entity_name, '{} must be a number!'.format(entity_name))
        if number >= max_value:
            if error_msg:
                raise RecruitException(message=error_msg, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise RecruitException(message='{} must be lesser than {}!'.format(entity_name, max_value), status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_number_gt_than_less_than(cls, number, min_value, max_value, entity_name=None, error_msg=None):
        cls.validate_number_gt_than(number, min_value, entity_name, error_msg)
        cls.validate_number_lt_than(number, max_value, entity_name, error_msg)

    @classmethod
    def validate_boolean(cls, flag, entity_name=None, error_msg=None):
        if flag in [None]:
            cls.__throw_exception(entity_name, error_msg)

    @classmethod
    def validate_obj(cls, obj, entity_name=None, error_msg=None):
        cls.__validate_validation_params(entity_name, error_msg)

        if obj in [None]:
            cls.__throw_exception(entity_name, error_msg)

    @classmethod
    def validate_enum(cls, enum, enum_class, entity_name=None, error_msg=None):
        cls.validate_obj(enum, entity_name, error_msg)
        if enum not in enum_class.__members__:
            raise RecruitException(message=enum + ' ' + entity_name + ' is not present!', status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_enum_v2(cls, enum, enum_class, entity_name=None, error_msg=None, raise_exception=True):
        cls.validate_obj(enum, entity_name, error_msg)
        if enum not in enum_class.__members__ and not any(enum == member.value for member in enum_class):
            if raise_exception:
                raise RecruitException(message=enum + ' ' + entity_name + ' is not present!', status=status.HTTP_400_BAD_REQUEST)
            else:
                return False
        else:
            return True

    @classmethod
    def validate_emails(cls, emails, entity_list_name=None, entity_name=None, empty_error_msg=None, invalid_error_msg=None):
        Validator.validate_empty_arr(emails, entity_list_name)
        for email in emails:
            Validator.validate_email(email, entity_name, empty_error_msg, invalid_error_msg)

    @classmethod
    def validate_email(cls, email, entity_name=None, empty_error_msg=None, invalid_error_msg=None,
                       use_adv_email_validation=True):
        cls.validate_string(email, entity_name, empty_error_msg)
        email = Transformers.trim(email)

        try:
            if use_adv_email_validation:
                bool_result = is_email(email, check_dns=True, diagnose=True)
                if bool_result.code == 0:
                    return True
                else:
                    raise ValidationError(email + ': ' + bool_result.description)
            else:
                validate_email(email)
        except ValidationError:
            error_str = ''
            if invalid_error_msg is None:
                error_str = email + " is an invalid email!"
            else:
                error_str = invalid_error_msg
            raise RecruitException(message=error_str, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_and_generate_emails_list_based_on_validity(cls, email, valid_emails, invalid_emails, entity_name=None,
                                                            empty_error_msg=None):
        cls.validate_string(email, entity_name, empty_error_msg)
        email = Transformers.trim(email)
        bool_result = is_email(email, check_dns=True, diagnose=True)
        if bool_result.code == 0:
            valid_emails[0] = True
        else:
            invalid_emails[0] = True

    @classmethod
    def validate_timestamp(cls, timestamp, entity_name):
        Validator.validate_obj(timestamp, entity_name)
        timestamp_type = type(timestamp)
        if timestamp_type is not timezone and timestamp_type is not datetime:
            raise RecruitException(message=entity_name + ' is not a valid "timezone" object',
                                   status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_phone_number(cls, country_code, phone_number, raise_exception=True):
        try:
            Validator.validate_number(country_code, 'Country code')
            Validator.validate_number(phone_number, 'Phone number')

            complete_phone_number = '+' + str(country_code) + str(phone_number)
            try:
                z = phonenumbers.parse(complete_phone_number, None)
                if not phonenumbers.is_possible_number(z) or not phonenumbers.is_valid_number(z):
                    raise RecruitException(message='Phone number: ' + complete_phone_number + ' is invalid!',
                                           status=status.HTTP_400_BAD_REQUEST)
                return True
            except Exception as ex:
                logger.error('Invalid phone number: {} -> error -> {}'.format(complete_phone_number, ex), ex)
                raise RecruitException(message='Phone number: ' + complete_phone_number + ' is invalid!',
                                       status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            if raise_exception is True:
                raise ex
            return False

    @classmethod
    def validate_and_get_file_type(cls, file, allowed_file_types, error_msg=None):
        file_type = FileUtil.get_file_type(file)

        cls.validate_file_type(allowed_file_types, file_type, error_msg)

        if file.size > MAX_FILE_UPLOAD_SIZE:
            raise RecruitException(message='Max file size can be: ' + MAX_FILE_UPLOAD_SIZE_STR,
                                   status=status.HTTP_400_BAD_REQUEST)

        return file_type

    @classmethod
    def validate_file_type(cls, allowed_file_types, file_type, error_msg=None):
        if not file_type:
            raise RecruitException(message='No file type found!', status=status.HTTP_400_BAD_REQUEST)
        if file_type not in allowed_file_types:
            error_str = ''
            if error_msg is None:
                error_str = '{} is not supported! Only'.format(file_type) + str(allowed_file_types) + " are allowed."
            else:
                error_str = error_msg
            raise RecruitException(message=error_str, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_request_for_file_and_get_file_type(cls, request, allowed_file_types, error_msg=None):
        if 'file' in request.FILES:
            file = request.FILES['file']
            if file:
                file_type = Validator.validate_and_get_file_type(file, allowed_file_types, error_msg)
                return file, file_type
        raise RecruitException(message='No file present in the request!', status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_time_gt_current_time(cls, time, error_msg):
        if time <= timezone.now():
            raise RecruitException(message=error_msg, status=status.HTTP_400_BAD_REQUEST)
        return time

    @classmethod
    def validate_time_lt_other_time(cls, smaller_time, bigger_time, error_msg):
        if smaller_time >= bigger_time:
            raise RecruitException(message=error_msg, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_expiry_time(cls, expiry_time, error_msg):
        return Validator.validate_time_gt_current_time(expiry_time, error_msg)

    @classmethod
    def validate_time_diff_lte_start_and_end(cls, start_time, end_time, duration, error_msg):
        if end_time.timestamp() - start_time.timestamp() < duration:
            raise RecruitException(message=error_msg, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_base64_string(cls, base64_str, entity_name):
        cls.validate_string(base64_str, entity_name)
        if ';base64,' not in base64_str:
            raise RecruitException(message='Not a valid base64 string!', status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_dict(cls, inp_dict, key, entity_name):
        Validator.validate_obj(inp_dict, entity_name)
        if not MapUtil.check_if_map_key_has_value(inp_dict, key):
            raise RecruitException(message='{} field must be present in the {}'.format(key, entity_name),
                                   status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_limit_offset(cls, request):
        limit = request.GET.get('limit', '1')
        limit = eval(limit)
        cls.validate_string(limit, 'Limit')
        offset = request.GET.get('offset', '0')
        offset = eval(offset)
        cls.validate_string(offset, 'Offset')

    @classmethod
    def validate_table_model(cls, main_table_name):
        if not inspect.isclass(main_table_name) and not issubclass(main_table_name, models.Model):
            raise RecruitException(message="{} does not exist",
                                   status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def __throw_exception(cls, entity_name, error_msg):
        error_str = None
        if error_msg is None:
            error_str = entity_name + " can't be empty!"
        else:
            error_str = error_msg
        raise RecruitException(message=error_str, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def __validate_validation_params(cls, entity_name, error_msg):
        if entity_name is None and error_msg is None:
            raise RecruitException(message="Both entity name and error message can't be empty!",
                                   status=status.HTTP_400_BAD_REQUEST)
