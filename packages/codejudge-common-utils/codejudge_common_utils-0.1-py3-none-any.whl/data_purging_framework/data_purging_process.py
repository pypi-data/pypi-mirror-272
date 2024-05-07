from abc import ABC, abstractmethod

from restapi.proctoring.models import AIProcStatus


def get_data_to_insert(records_to_delete, all_fields):
    all_data = []
    for record in records_to_delete:
        data = {}
        for field in all_fields:
            field_value = getattr(record, field)
            data[field] = field_value
        all_data.append(data)

    return all_data


class DataPurgingInterface(ABC):

    @abstractmethod
    def get_stale_records(self, main_table_name, archive_table_name, interval_start_date, interval_end_date, all_fields, prev_size, size):
        pass

    @abstractmethod
    def get_count_of_records_between_interval_dates(self, interval_start_date, interval_end_date, main_table_name):
        pass


class AIProctoringPurge(DataPurgingInterface):

    def get_stale_records(self, main_table_name, archive_table_name, interval_start_date, interval_end_date, all_fields, prev_size, size):
        records_to_delete = main_table_name.objects.filter(proc_status=AIProcStatus.COMPLETED.value)[prev_size:size]
        all_fields_and_value = get_data_to_insert(records_to_delete, all_fields)
        return all_fields_and_value, records_to_delete

    def get_count_of_records_between_interval_dates(self, interval_start_date, interval_end_date, main_table_name):
        total_count = main_table_name.objects.filter(proc_status=AIProcStatus.COMPLETED.value).count()
        return total_count




