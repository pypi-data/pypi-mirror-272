import json
from collections import OrderedDict

from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict

from restapi.common.string_util import StringUtil
from restapi.common.validators import Validator


class JsonUtil:

    @classmethod
    def convert_obj_to_json(cls, obj):
        if obj:
            return json.dumps(obj.__dict__, cls=DjangoJSONEncoder)
        return obj

    @classmethod
    def convert_obj_to_dict(cls, obj):
        if obj:
            return model_to_dict(obj)
        return obj

    @classmethod
    def convert_obj_to_json_v2(cls, obj):
        if obj:
            return json.dumps(model_to_dict(obj), cls=DjangoJSONEncoder)
        return obj

    @classmethod
    def convert_dict_to_json(cls, dict, check_for_none_only=False):
        if (check_for_none_only is True and dict is not None) or dict:
            return json.dumps(dict, cls=DjangoJSONEncoder)
        return dict

    @classmethod
    def convert_list_objs_to_json(cls, objs):
        if objs:
            return json.dumps([obj.__dict__ for obj in objs], cls=DjangoJSONEncoder)
        return objs

    @classmethod
    def convert_list_objs_to_dict(cls, objs):
        if objs:
            return [obj.__dict__ for obj in objs]
        return objs

    @classmethod
    def convert_bytes_to_dict(cls, json_bytes):
        json_str = StringUtil.get_str_from_bytes(json_bytes)
        return cls.convert_json_to_dict(json_str)

    @classmethod
    def convert_json_to_dict(cls, json_str):
        if json_str and not isinstance(json_str, dict):
            return json.loads(json_str, object_pairs_hook=OrderedDict)
        return json_str

    @classmethod
    def is_valid(cls, json_str):
        try:
            json_object = json.loads(json_str)
        except ValueError as e:
            return False
        return True
