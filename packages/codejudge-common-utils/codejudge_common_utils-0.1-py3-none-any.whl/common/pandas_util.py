from collections import OrderedDict


class PandasUtil:

    @classmethod
    def convert_data_frame_to_dict_list(cls, data_frame):
        data_frame_dict = data_frame.to_dict()
        headers = list(data_frame_dict.keys())

        all_candidates_dict = {}
        for header in headers:
            column_entries = data_frame_dict[header]
            for key, value in column_entries.items():
                if all_candidates_dict.get(key) is None:
                    all_candidates_dict[key] = OrderedDict()
                all_candidates_dict[key][header] = value
        return all_candidates_dict.values()