class MapUtil:

    @classmethod
    def is_valid(cls, input_map):
        return input_map and len(input_map) > 0

    @classmethod
    def check_if_map_key_has_value(cls, inp_map, key):
        return inp_map and key in inp_map and inp_map[key]

    @classmethod
    def check_if_map_has_key(cls, inp_map, key):
        return inp_map and key in inp_map
