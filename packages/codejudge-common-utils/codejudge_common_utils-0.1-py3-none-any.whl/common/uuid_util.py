import uuid
from builtins import str, ValueError
from uuid import UUID

from rest_framework import status

from restapi.common.list_util import ListUtil
from restapi.common.validators import Validator
from restapi.exception.exception import RecruitException


class UUIDUtil:

    @classmethod
    def convert_to_string(cls, inp_uuid: UUID):
        return cls.validate_and_transform_uuid(str(inp_uuid))

    @classmethod
    def validate_and_transform_uuids(cls, test_uuids):
        transformed_uuids = []
        if ListUtil.is_valid(test_uuids):
            for test_uuid in test_uuids:
                test_uuid = cls.validate_and_transform_uuid(test_uuid)
                transformed_uuids.append(test_uuid)
            return transformed_uuids
        raise RecruitException(message='No test uuids present!', status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_uuid(cls, val, msg=None):
        if msg is None:
            msg = 'Invalid key!'
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            raise RecruitException(message=msg, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_and_transform_uuid(cls, uuid, msg=None, validate_uuid=True):
        Validator.validate_string(uuid, 'UUID')
        if validate_uuid:
            cls.validate_uuid(uuid, msg)
        return uuid.replace('-', '')

    @classmethod
    def validate_and_transform_uuid_string(cls, uuid):
        Validator.validate_string(uuid, 'UUID')
        return uuid.replace('-', '')

    @classmethod
    def get_uuid(cls):
        return cls.validate_and_transform_uuid(str(uuid.uuid4()))
