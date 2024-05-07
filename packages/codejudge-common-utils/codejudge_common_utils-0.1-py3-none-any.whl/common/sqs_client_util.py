import boto3
from botocore.config import Config

from codejudgework.settings import REGION_NAME, AWS_SQS_ACCESS_KEY, AWS_SQS_SECRET_KEY


class SqsClientUtil:

    @staticmethod
    def get_config():
        return Config(connect_timeout=5, read_timeout=180, retries={'max_attempts': 0})

    @staticmethod
    def create_client():
        client = boto3.client('sqs', aws_access_key_id=AWS_SQS_ACCESS_KEY,
                              aws_secret_access_key=AWS_SQS_SECRET_KEY, region_name=REGION_NAME,
                              config=SqsClientUtil.get_config())
        return client

    @staticmethod
    def create_resource():
        resource = boto3.resource('sqs', aws_access_key_id=AWS_SQS_ACCESS_KEY,
                                  aws_secret_access_key=AWS_SQS_SECRET_KEY, region_name=REGION_NAME,
                                  config=SqsClientUtil.get_config())
        return resource
