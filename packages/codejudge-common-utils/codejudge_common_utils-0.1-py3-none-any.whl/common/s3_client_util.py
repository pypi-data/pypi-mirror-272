import boto3
from botocore.config import Config

from codejudgework.settings import REGION_NAME, AWS_S3_ACCESS_KEY, AWS_S3_SECRET_KEY


class S3ClientUtil:

    @staticmethod
    def get_config():
        return Config(connect_timeout=5, read_timeout=180, retries={'max_attempts': 0})

    @staticmethod
    def create_client():
        client = boto3.client('s3', aws_access_key_id=AWS_S3_ACCESS_KEY,
                              aws_secret_access_key=AWS_S3_SECRET_KEY, region_name=REGION_NAME,
                              config=S3ClientUtil.get_config())
        return client

    @staticmethod
    def create_resource():
        resource = boto3.resource('s3', aws_access_key_id=AWS_S3_ACCESS_KEY,
                                  aws_secret_access_key=AWS_S3_SECRET_KEY, region_name=REGION_NAME,
                                  config=S3ClientUtil.get_config())
        return resource
