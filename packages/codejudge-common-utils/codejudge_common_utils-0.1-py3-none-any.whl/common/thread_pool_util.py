import logging
import time
from math import floor
from multiprocessing.pool import ThreadPool

from rest_framework import status

from restapi.exception.exception import RecruitException

logger = logging.getLogger(__name__)


class ThreadPoolUtil:

    @classmethod
    def run_async(cls, all_items, max_pool_size, func):
        logger.info(
            'running items of size: {} in a thread pool in async fashion with max pool size: {}'.format(len(all_items),
                                                                                                        max_pool_size))
        items_list = cls.get_items_for_thread_pool(all_items, max_pool_size)
        return cls.run_in_process_thread_pool_async(items_list, func)

    @classmethod
    def run_and_combine_results_map(cls, all_items, max_pool_size, func):
        combined_item_map = dict()
        item_map_list = cls.run(all_items, max_pool_size, func)
        for item_map in item_map_list:
            for key in item_map:
                combined_item_map[key] = item_map[key]

        return combined_item_map

    @classmethod
    def run_in_process_thread_pool_async(cls, items_list, func):
        pool = cls.__validate_and_get_thread_pool(func, items_list)
        response = pool.map_async(func, items_list)
        time.sleep(1)
        pool.terminate()
        pool.close()
        logger.info('ran the thread pool in async fashion..')
        return response

    @classmethod
    def run(cls, all_items, max_pool_size, func):
        logger.info('running items of size: {} in a thread pool with max pool size: {}'.format(len(all_items),
                                                                                               max_pool_size))
        items_list = cls.get_items_for_thread_pool(all_items, max_pool_size)
        return cls.run_in_process_thread_pool(items_list, func)

    @classmethod
    def get_items_for_thread_pool(cls, all_items, max_pool_size):
        if not all_items or len(all_items) <= 0:
            raise RecruitException(message='No items found!', status=status.HTTP_400_BAD_REQUEST)
        if not max_pool_size:
            raise RecruitException(message='Max pool size not defined!', status=status.HTTP_400_BAD_REQUEST)

        logger.info('get items of size: {} for a thread pool with max pool size: {}'.format(len(all_items),
                                                                                            max_pool_size))
        total_items = len(all_items)
        total_processes = max_pool_size
        items_per_process = floor(total_items / total_processes)
        remaining_items = total_items % max_pool_size

        if items_per_process == 0:
            total_processes = remaining_items

        items_per_thread_list = []
        new_start_index = 0
        for iter in range(0, total_processes):
            start_index = new_start_index
            if remaining_items > 0:
                new_start_index = start_index + items_per_process + 1
            else:
                new_start_index = start_index + items_per_process

            spliced_items = all_items[start_index:new_start_index]
            items_per_thread_list.append(spliced_items)
            remaining_items -= 1

        return items_per_thread_list

    @classmethod
    def run_in_process_thread_pool(cls, items_list, func):
        if not items_list or len(items_list) <= 0:
            raise RecruitException(message='No items found for running in thread pool..',
                                   status=status.HTTP_400_BAD_REQUEST)
        if not func:
            raise RecruitException(message='No function found for running in thread pool..',
                                   status=status.HTTP_400_BAD_REQUEST)

        logger.info('running items of size (thread pool size): {} in a thread pool'.format(len(items_list)))
        pool = ThreadPool(processes=len(items_list))
        response = pool.map(func, items_list)
        pool.close()
        pool.join()
        return response

    @classmethod
    def __validate_and_get_thread_pool(cls, func, items_list):
        if not items_list or len(items_list) <= 0:
            raise RecruitException(message='No items found for running in thread pool..',
                                   status=status.HTTP_400_BAD_REQUEST)
        if not func:
            raise RecruitException(message='No function found for running in thread pool..',
                                   status=status.HTTP_400_BAD_REQUEST)
        logger.info('running items of size (thread pool size): {} in a thread pool'.format(len(items_list)))
        pool = ThreadPool(processes=len(items_list))
        return pool

