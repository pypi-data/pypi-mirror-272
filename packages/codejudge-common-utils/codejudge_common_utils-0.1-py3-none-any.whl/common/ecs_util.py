import logging
from time import sleep

import boto3
from rest_framework import status

from codejudgework.settings import REGION_NAME, AWS_ECS_KEY, AWS_ECS_SECRET
from restapi.exception.exception import RecruitException

logger = logging.getLogger(__name__)


class ECSServiceUtil:

    MAX_RETRIES = 5
    SLEEP_TIME_FOR_SERVICE_UPDATE = 20

    @classmethod
    def get_ecs_client(cls):
        return boto3.client('ecs', aws_access_key_id=AWS_ECS_KEY, aws_secret_access_key=AWS_ECS_SECRET, region_name=REGION_NAME)

    @classmethod
    def get_service_details(cls, cluster_name, service_name=None, service_arn=None):
        ecs_client = cls.get_ecs_client()

        if service_arn is not None:
            logger.info('got request to get details of service arn -> ({}) of cluster -> ({})'.format(service_name, cluster_name))
            service_details = ecs_client.describe_services(cluster=cluster_name, services=[service_arn])
            return service_details['services'][0]

        if service_name is None:
            raise RecruitException(message="Both service name and service arn cannot be None!!!",
                                   status=status.HTTP_400_BAD_REQUEST)

        logger.info('got request to get details of service name -> ({}) of cluster -> ({})'.format(service_name, cluster_name))
        services_list = ecs_client.list_services(cluster=cluster_name)['serviceArns']
        if services_list:
            for service in services_list:
                service_name_from_details = service.split('/')[-1]
                if service_name_from_details == service_name:
                    service_details = ecs_client.describe_services(cluster=cluster_name, services=[service])
                    return service_details['services'][0]
        else:
            raise RecruitException(message="No services found !!",
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def update_service_details(cls, cluster_name, service_name, num_of_tasks, service_arn):
        logger.info('updating the number of tasks: {} of service -> {}'.format(num_of_tasks, service_name))
        ecs_client = cls.get_ecs_client()
        ecs_client.update_service(cluster=cluster_name, service=service_name, desiredCount=num_of_tasks)
        cls.__wait_for_service_update(cluster_name, service_arn)
        logger.info("service {} updated successfully".format(service_name))


    @classmethod
    def __wait_for_service_update(cls, cluster_name, service_arn):
        running_count = 1
        desired_count = 0
        max_tries = ECSServiceUtil.MAX_RETRIES
        while desired_count != running_count and max_tries > 0:
            sleep(ECSServiceUtil.SLEEP_TIME_FOR_SERVICE_UPDATE)
            response = cls.get_service_details(cluster_name, None, service_arn)
            running_count = response['runningCount']
            desired_count = response['desiredCount']
            max_tries -= 1
        if max_tries == 0:
            raise RecruitException(message="Could not update the Service! Manual check needed!",
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR, send_email=True)
