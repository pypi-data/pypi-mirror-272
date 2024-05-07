
class ModelUtil:

    @classmethod
    def get_all_field_names(cls, model, ignore_fields=[], prepend_table_name=False, table_name=''):
        prefix = table_name + '.' if prepend_table_name is True else ''
        field_names = []
        for f in model._meta.get_fields():
            field_name = f.name
            if field_name not in ignore_fields:
                field_names.append(prefix + f.name)
        return field_names
