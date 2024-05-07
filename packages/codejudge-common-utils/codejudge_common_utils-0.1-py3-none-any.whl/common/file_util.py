import logging
import base64
import os
import shutil
import subprocess
import urllib.request

import fitz
import docx2txt
from django.core.files.base import ContentFile
from rest_framework import status

from codejudgework.settings import ENVIRONMENT
from restapi.common.enums import Environment
from restapi.common.s3_file_util import S3FileUtil
from restapi.exception.exception import RecruitException

logger = logging.getLogger(__name__)


class FileUtil:
    PDF_EXTENSION = '.pdf'
    DOCX_EXTENSION = '.docx'
    RTF_EXTENSION = '.rtf'
    TXT_EXTENSION = '.txt'
    DOC_EXTENSION = '.doc'

    @staticmethod
    def get_file_content(file, file_type):
        return file.read().decode('utf-8')
        # if file_type == 'csv':
        #     return file.read().decode('utf-8')
        # else:
        #     return file.read()

    @classmethod
    def get_all_extensions(cls):
        return [cls.RTF_EXTENSION, cls.DOCX_EXTENSION, cls.TXT_EXTENSION, cls.DOC_EXTENSION, cls.DOCX_EXTENSION]

    @staticmethod
    def get_file_type(file):
        content_type = file.content_type
        if content_type:
            return content_type.rsplit('/', 1)[-1]
        else:
            return None

    @staticmethod
    def get_file_extension(file_name):
        if file_name:
            last_dot_index = file_name.rfind('.')
            return file_name[-(len(file_name) - last_dot_index):]
        return None

    @staticmethod
    def base64_file(data, name=None):
        _format, _img_str = data.split(';base64,')
        _name, ext = _format.split('/')
        if not name:
            name = _name.split(":")[-1]

        file_name = '{}.{}'.format(name, ext)
        return ContentFile(base64.b64decode(_img_str), name=file_name), file_name, ext

    @staticmethod
    def get_uuid_file_name(file_name, uuid):
        return os.path.splitext(file_name)[0] + '-' + uuid + os.path.splitext(file_name)[1]

    @staticmethod
    def get_content_type_to_file_extensions_map():
        return {
            'pdf': ['.pdf'],
            'msword': ['.dot', '.doc'],
            'docx': ['.docx'],
            'vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
            'vnd.openxmlformats-officedocument.wordprocessingml.template': ['.dotx'],
            'vnd.ms-excel': ['.xls', '.xlt', '.xla'],
            'vnd.openxmlformats-officedocument.spreadsheetml.template': ['.xltx'],
            'vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
            'vnd.ms-powerpoint': ['.ppt', '.pot', '.pps', '.ppa'],
            'vnd.ms-word.document.macroEnabled.12': ['.docm'],
            'vnd.ms-word.template.macroEnabled.12': ['.dotm'],
            'vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
            'vnd.openxmlformats-officedocument.presentationml.template': ['.potx'],
            'vnd.openxmlformats-officedocument.presentationml.slideshow': ['.ppsx'],
            'vnd.ms-powerpoint.addin.macroEnabled.12': ['.ppam'],
            'vnd.ms-powerpoint.presentation.macroEnabled.12': ['.pptm'],
            'vnd.ms-powerpoint.template.macroEnabled.12': ['.potm'],
            'vnd.ms-powerpoint.slideshow.macroEnabled.12': ['.ppsm'],
            'vnd.ms-excel.sheet.macroEnabled.12': ['.xlsm'],
            'vnd.ms-excel.template.macroEnabled.12': ['.xltm'],
            'vnd.ms-excel.addin.macroEnabled.12': ['.xlam'],
            'vnd.ms-excel.sheet.binary.macroEnabled.12': ['.xlsb'],
            'vnd.ms-access': ['.mdb']
        }

    @staticmethod
    def get_file_extensions_by_content_types(types):
        extensions = []
        content_type_to_extensions_map = FileUtil.get_content_type_to_file_extensions_map()
        for content_type in types:
            extensions.extend(content_type_to_extensions_map.get(content_type))
        return extensions

    @classmethod
    def get_file_content_from_url(cls, url):
        with urllib.request.urlopen(url) as f:
            content = f.read().decode('utf-8')
            return content

    @classmethod
    def get_file_content_from_urls(cls, urls):
        logger.info("got request to get content from the {} url".format(len(urls)))
        contents = {}
        for url in urls:
            with urllib.request.urlopen(url) as f:
                content = f.read().decode('utf-8')
                contents[url] = content
        return contents

    @classmethod
    def delete_file(cls, file_path, raise_exception):
        logger.info('got request to remove file if exists: {} and raise exception flag: {}'.format(file_path,
                                                                                                   raise_exception))
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as ex:
                logging.error('Unable to delete file path: {}'.format(file_path))
                if raise_exception:
                    raise RecruitException(message="Unable to delete file {}".format(file_path), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def delete_folder(cls, folder_name, raise_exception):
        try:
            shutil.rmtree(folder_name)
            logger.info('Deleted {}'.format(folder_name))
        except Exception as ex:
            logging.error('Unable to delete folder {}'.format(folder_name))
            if raise_exception:
                raise ex

    @classmethod
    def extract_text_from_docx(cls, docx_file_name):
        text = docx2txt.process(docx_file_name)
        if not text:
            cls.delete_file(docx_file_name, True)
            raise RecruitException(message="The uploaded file is empty.",
                                   status=status.HTTP_400_BAD_REQUEST)
        return text

    @classmethod
    def extract_text_from_pdf(cls, pdf_file):
        doc = fitz.open(pdf_file)
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text("text")
        doc.close()
        if not text:
            cls.delete_file(pdf_file, True)
            raise RecruitException(message="The uploaded file is empty.",
                                   status=status.HTTP_400_BAD_REQUEST)
        return text

    @classmethod
    def convert_any_document_to_docx(cls, file_name, ext):
        try:
            command = "/opt/libreoffice7.6/program/soffice" if ENVIRONMENT in [Environment.DEV.value, Environment.PROD.value] else "soffice"
            subprocess.check_output([command, '--headless', '--convert-to', 'docx', file_name])
            docx_file_name = file_name.split(ext)[0] + cls.DOCX_EXTENSION
            return docx_file_name
        except subprocess.CalledProcessError as e:
            raise e

    @classmethod
    def download_and_convert_and_extract_file(cls, file_name, s3_url, is_url, s3_bucket_name, s3_key):
        logger.info("Got request to download, convert, "
                    "and extract data from file. File name: {}, S3 url: {}, S3 bucket name: {}, S3 key: {}".
                    format(file_name, s3_url, s3_bucket_name, s3_key))
        try:
            if is_url:
                S3FileUtil.download_s3_file_by_s3_url(s3_url, file_name, s3_bucket_name, s3_key)
            ext = FileUtil.get_file_extension(file_name)
            if ext == cls.PDF_EXTENSION:
                text = cls.extract_text_from_pdf(file_name)
            elif ext in [cls.RTF_EXTENSION, cls.TXT_EXTENSION, cls.DOC_EXTENSION]:
                file_name = cls.convert_any_document_to_docx(file_name, ext)
                text = cls.extract_text_from_docx(file_name)
            elif ext == cls.DOCX_EXTENSION:
                text = cls.extract_text_from_docx(file_name)
            else:
                all_extensions = cls.get_all_extensions()
                raise RecruitException(message="The uploaded file is not valid. Please make sure "
                                               "the file type is one of the following: {}".format(all_extensions),
                                       status=status.HTTP_406_NOT_ACCEPTABLE, send_email=False)
            cls.delete_file(file_name, True)
            return text
        except RecruitException as e:
            raise e
        except subprocess.CalledProcessError as e:
            logger.info(e.args)
            raise RecruitException(message="Couldn't parse file. Please try again!",
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)
