import logging
import re
from datetime import datetime, timedelta
from multiprocessing.pool import ThreadPool
from urllib.parse import urlparse

from botocore.signers import CloudFrontSigner
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from rest_framework import status

from restapi.common.map_util import MapUtil
from restapi.common.list_util import ListUtil
from restapi.common.s3_client_util import S3ClientUtil
from restapi.exception.exception import RecruitException

logger = logging.getLogger(__name__)


class S3FileUtil:

    @staticmethod
    def upload_multiple_files(bucket_name, folder_name, source_file_paths, is_public=False):
        if not bucket_name or not source_file_paths:
            raise RecruitException(message='Bucket name and source file paths are required!',
                                   status=status.HTTP_400_BAD_REQUEST)

        transformed_file_paths = []
        for file_path in source_file_paths:
            transformed_file_paths.append({
                'bucket_name': bucket_name,
                'key': S3FileUtil.get_file_key(file_path, folder_name),
                'file_name': file_path,
                'is_public': is_public
            })
        try:
            pool = ThreadPool(processes=10)
            return pool.map(S3FileUtil.upload, transformed_file_paths)
        except Exception as ex:
            logger.error("bulk file upload failed!", ex)
            raise RecruitException(message='Couldn\'t upload file!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def upload_file(bucket_name, folder_name, dest_file_name, source_file_path, is_public):
        if not bucket_name or not dest_file_name or not source_file_path:
            raise RecruitException(message='Bucket name, file name and source file path are required!',
                                   status=status.HTTP_400_BAD_REQUEST)

        try:
            return S3FileUtil.upload({
                'bucket_name': bucket_name,
                'file_name': source_file_path,
                'key': S3FileUtil.get_file_key(dest_file_name, folder_name),
                'is_public': is_public
            })
        except Exception as ex:
            logger.error("single file upload failed!", ex)
            raise RecruitException(message='Couldn\'t upload file!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def upload_file_in_memory(bucket_name, folder_name, dest_file_name, file, is_public):
        if not bucket_name or not dest_file_name or not file:
            raise RecruitException(message='Bucket name, file name and file are required!',
                                   status=status.HTTP_400_BAD_REQUEST)

        try:
            return S3FileUtil.upload_in_memory({
                'bucket_name': bucket_name,
                'file': file,
                'key': S3FileUtil.get_file_key(dest_file_name, folder_name),
                'is_public': is_public
            })
        except Exception as ex:
            logger.error("single file upload failed!", ex)
            raise RecruitException(message='Couldn\'t upload file!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_s3_file(bucket_name, folder_name, dest_file_name):
        s3 = S3FileUtil.__get_s3_client()
        file = s3.get_object(Bucket=bucket_name, Key=S3FileUtil.get_file_key(dest_file_name, folder_name))
        return file

    @staticmethod
    def get_file_name(s3_url):
        if s3_url:
            return s3_url.split('/')[-1]
        raise RecruitException(message='Invalid s3 url!', status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_file_key(dest_file_name, folder_name):
        if folder_name:
            dest_file_name = folder_name + '/' + dest_file_name
        return dest_file_name

    @staticmethod
    def upload(file_metadata):
        try:
            logger.info("got request to upload file with metadata: " + str(file_metadata))
            args = dict()
            if 'is_public' in file_metadata and file_metadata['is_public']:
                args['ACL'] = 'public-read'
            S3FileUtil.__get_s3_client().upload_file(file_metadata['file_name'], file_metadata['bucket_name'],
                                                     file_metadata['key'], ExtraArgs=args)
            s3_path = S3FileUtil.get_s3_path(file_metadata)
            logger.info("Uploaded filename: " + s3_path + ' successfully!')
            return s3_path
        except Exception as ex:
            logger.error("file upload in a thread pool failed!", ex)
            raise RecruitException(message='Couldn\'t upload file!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def upload_in_memory(file_metadata):
        try:
            logger.info("got request to upload file with metadata: " + str(file_metadata))
            resource = S3FileUtil.__get_s3_resource()

            args = dict()
            if 'is_public' in file_metadata and file_metadata['is_public']:
                args = dict(ACL='public-read')
            resource.Bucket(file_metadata['bucket_name']).put_object(Key=file_metadata['key'],
                                                                     Body=file_metadata['file'],
                                                                     **args)
            s3_path = S3FileUtil.get_s3_path(file_metadata)
            logger.info("Uploaded file: " + s3_path + ' successfully!')
            return s3_path
        except Exception as ex:
            logger.error("file upload in a thread pool failed!", ex)
            raise RecruitException(message='Couldn\'t upload file!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_s3_path(file_metadata):
        return 's3://' + file_metadata['bucket_name'] + '/' + file_metadata['key']

    @staticmethod
    def get_https_path(bucket_name, key):
        return "https://" + bucket_name + ".s3.amazonaws.com/" + key

    @staticmethod
    def get_signature_data_to_upload_file(bucket_name, folder_name, file_name, expiry):
        if not (bucket_name and folder_name and file_name and expiry):
            raise RecruitException(message='Bucket name, file name and folder name and expiry are required!',
                                   status=status.HTTP_400_BAD_REQUEST)
        try:
            data = S3FileUtil.__get_s3_client().generate_presigned_post(
                bucket_name,
                S3FileUtil.get_file_key(file_name, folder_name),
                ExpiresIn=expiry,
            )
            return data
        except Exception as ex:
            logger.error("prsigned url to upload file failed!", ex)
            raise RecruitException(message='Couldn\'t upload file!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_cloudfront_signed_url(cf_url, cf_distribution_private_key, cf_distribution_key_id, expiry):
        def rsa_signer(message):
            private_key = serialization.load_pem_private_key(
                bytes(cf_distribution_private_key, encoding='utf-8'),
                password=None,
                backend=default_backend()
            )
            return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())
        cf_distribution_private_key = cf_distribution_private_key.replace("\\n", "\n").replace("\\r", "\r")
        if not (cf_url and cf_distribution_key_id and cf_distribution_private_key and expiry):
            raise RecruitException(
                message='cf url, cf distribution key id and cf distribution private key and expiry are required!',
                status=status.HTTP_400_BAD_REQUEST)
        try:
            cloudfront_signer = CloudFrontSigner(cf_distribution_key_id, rsa_signer)

            # Create a signed url that will be valid until the specfic expiry date
            # provided using a canned policy.
            signed_url = cloudfront_signer.generate_presigned_url(cf_url, date_less_than=expiry)
            return signed_url
        except Exception as ex:
            logger.error("prsigned url to get file from cloudfront failed!", ex)
            raise RecruitException(message='Couldn\'t get file!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_files_from_folder(bucket_name, folder_name, limit, start_after, sort_by=None):
        logger.info('got request to get file names via bucket: {}, folder: {}, limit: {}, start_after: {} '
                    'and sort by: {}'.format(bucket_name, folder_name, limit, start_after, sort_by))
        s3_client = S3FileUtil.__get_s3_client()
        files = []
        params = dict(Bucket=bucket_name, Prefix=folder_name, MaxKeys=limit)
        if start_after:
            params['StartAfter'] = start_after
        objects = s3_client.list_objects_v2(**params)
        if MapUtil.check_if_map_key_has_value(objects, 'Contents'):
            for key in objects['Contents']:
                files.append(S3FileUtil.get_https_path(bucket_name, key['Key']))
            return files
        return []

    @staticmethod
    def get_files_from_folder_v2(bucket_name, folder_name, limit, start_after):
        logger.info('got request to get file names via bucket: {}, folder: {}, limit: {}, start_after: {}'.format(bucket_name, folder_name, limit, start_after))
        s3_client = S3FileUtil.__get_s3_client()
        files = []
        try:
            params = dict(Bucket=bucket_name, Prefix=folder_name, MaxKeys=limit)
            if start_after:
                params['StartAfter'] = start_after
            truncated = True
            total_files = 0
            current_start_after = start_after
            if limit < 0:
                raise RecruitException(message="Invalid value for 'limit' parameter. 'limit' must be a positive integer.", status=status.HTTP_400_BAD_REQUEST)
            elif limit == 0:
                return files
            while truncated and total_files < limit:
                response = s3_client.list_objects_v2(**params)
                if MapUtil.is_valid(response) and MapUtil.check_if_map_key_has_value(response, 'Contents') and ListUtil.is_valid(response['Contents']):
                    for file in response['Contents']:
                        if MapUtil.is_valid(file) and MapUtil.check_if_map_key_has_value(file, 'Key') and file['Size'] > 0:
                            files.append(S3FileUtil.get_https_path(bucket_name, file['Key']))
                            current_start_after = file['Key']
                            total_files += 1
                truncated = response.get('IsTruncated', False)
                if truncated:
                    params['ContinuationToken'] = response['NextContinuationToken']
            return files, current_start_after
        except Exception as ex:
            logger.error("An error occurred while retrieving files from S3: {}", ex)
            raise RecruitException(message=str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_s3_file_from_s3_or_https_url_and_read(s3_or_https_url):
        logger.info('got request to get s3 file from s3 or https url: {}'.format(s3_or_https_url))
        metadata = S3FileUtil.get_file_metadata(s3_or_https_url)
        bucket_name = metadata['bucket_name']
        key = metadata['key']
        s3 = S3FileUtil.__get_s3_resource()
        bucket = s3.Bucket(bucket_name)
        s3_file = bucket.Object(key)
        return s3_file.get()['Body'].read()

    @staticmethod
    def get_s3_file_and_read(bucket_name, key):
        logger.info('got request to get s3 file from bucket name: {}, key: {}'.format(bucket_name, key))
        s3 = S3FileUtil.__get_s3_resource()
        bucket = s3.Bucket(bucket_name)
        s3_file = bucket.Object(key)
        return s3_file.get()['Body'].read()

    @staticmethod
    def get_file_metadata(s3_url):
        if s3_url:
            s3_scheme = 's3://'
            https_scheme = 'https://'
            if s3_scheme in s3_url:
                s3_url = s3_url.replace(s3_scheme, '')
                s3_url_split = s3_url.split('/')
                bucket_name = s3_url_split[0]
                key = "/".join(s3_url_split[1:])
                return {
                    'bucket_name': bucket_name,
                    'key': key
                }
            elif https_scheme in s3_url:
                match = re.search('^https?://s3.([^.]+).amazonaws.com/([^\/]+)', s3_url)
                if match:
                    bucket_name = match.group(2)
                    bucket_pos = s3_url.find(bucket_name, 0)
                    key = s3_url.replace(s3_url[0:bucket_pos + len(bucket_name) + 1], '')
                else:
                    s3_url = s3_url.replace(https_scheme, '')
                    first_backslash_pos = s3_url.find("/", 0)
                    bucket_name = s3_url[0: first_backslash_pos].replace('.s3.amazonaws.com', '')
                    key = s3_url[first_backslash_pos + 1:]
                return {
                    'bucket_name': bucket_name,
                    'key': key
                }
            raise RecruitException(message='Invalid s3 url!', status=status.HTTP_400_BAD_REQUEST)
        raise RecruitException(message='S3 Url not present!', status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def download_s3_file_by_s3_url(s3_url, file_path, bucket_name, key):
        logger.info('got request to download s3 file from s3_url: {} to file path: {}'.format(s3_url, file_path))
        s3 = S3FileUtil.__get_s3_client()
        if bucket_name is None and key is None:
            bucket_name, key = S3FileUtil.get_bucket_name_and_key_from_url(s3_url)
        try:
            s3.download_file(bucket_name, key, file_path)
            return True
        except Exception as e:
            raise RecruitException(message='Invalid url!', status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_bucket_name_and_key_from_url(s3_url):
        logger.info("Got request to get s3 bucket name and s3 key from {}".format(s3_url))
        parsed_url = urlparse(s3_url)
        s3_bucket_name = parsed_url.netloc.split('.')[0]
        s3_key = parsed_url.path.lstrip('/')
        return s3_bucket_name, s3_key

    @staticmethod
    def __get_s3_client():
        return S3ClientUtil.create_client()

    @staticmethod
    def __get_s3_resource():
        return S3ClientUtil.create_resource()
