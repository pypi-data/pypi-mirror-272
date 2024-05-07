import logging

from rest_framework import status

from restapi.common.sqs_client_util import SqsClientUtil
from restapi.exception.exception import RecruitException

logger = logging.getLogger(__name__)


class SqsUtil:

    @staticmethod
    def send_message(queue_url, messages):
        try:
            logger.info("got request to push message: {} to sqs queue: {}".format(messages, queue_url))
            client = SqsUtil.__get_sqs_client()
            responses = []
            for message in messages:
                response = client.send_message(QueueUrl=queue_url, MessageBody=message)
                responses.append(response)
                logger.info("Message sent to queue: {} with response: {}".format(queue_url, response))
            return responses
        except Exception as ex:
            logger.error("push message to SQS in a thread pool failed!", ex)
            raise RecruitException(message='Couldn\'t push message: {}'.format(ex),
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def __get_sqs_client():
        return SqsClientUtil.create_client()

    @staticmethod
    def __get_sqs_resource():
        return SqsClientUtil.create_resource()
