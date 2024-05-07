from restapi.common.list_util import ListUtil
from restapi.common.string_util import StringUtil


class Transformers:

    @classmethod
    def transform_if_none(cls, var, transform_to='NA'):
        if var is None:
            return transform_to
        return var

    @classmethod
    def handle_no_key(cls, var, key, transform_to=None):
        if var is not None and key is not None:
            if key in var:
                return var[key]
        return transform_to

    @classmethod
    def handle_no_key_and_value_is_not_none(cls, var, key, transform_to=None):
        if var is not None and key is not None:
            if key in var and var[key] is not None and var[key] != '':
                return var[key]
        return transform_to

    @classmethod
    def handle_no_key_and_set(cls, output, output_key, var, key):
        if var is not None and key is not None:
            if key in var:
                output[output_key] = var[key]

    @classmethod
    def handle_if_null(cls, var):
        if var:
            if var == 'null':
                return None
        return var

    @classmethod
    def transform_if_zero(cls, var, transform_to='NA'):
        if var is None or var == 0:
            return transform_to
        return var

    @classmethod
    def transform_if_minus_one(cls, var, transform_to='NA'):
        if var is None or var == -1:
            return transform_to
        return var

    @classmethod
    def to_lower_case_and_trim(cls, var):
        if var and isinstance(var, str):
            return var.lower().strip()
        return var

    @classmethod
    def trim(cls, var):
        if var:
            return var.strip()
        return var

    @classmethod
    def split_and_trim(cls, input, delimiter=','):
        if input:
            return [x.strip() for x in input.split(delimiter)]
        return input

    @classmethod
    def transform_email(cls, email, domains_for_dot_removal=[]):
        if email:
            if ListUtil.is_valid(domains_for_dot_removal):
                for domain in domains_for_dot_removal:
                    if domain in email:
                        email = email.replace(domain, '')
                        return email.replace('.', '') + domain
            email = email.lower()
        return email
