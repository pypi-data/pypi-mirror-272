from restapi.common.validators import Validator


class ServiceUtil:

    @classmethod
    def get_service(cls, calendar_service_mapping, type):
        Validator.validate_obj(calendar_service_mapping, 'Type to Service Mapping')
        Validator.validate_obj(type, 'Type')
        return calendar_service_mapping[type]()
