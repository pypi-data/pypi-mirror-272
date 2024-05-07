import os

import cv2

from restapi.common.uuid_util import UUIDUtil


class VideoUtil(object):

    @classmethod
    def get_frame(cls, url, sec, file_name):
        vidcap = cv2.VideoCapture(url)
        vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        hasFrames, image = vidcap.read()
        file_name_local = None
        if hasFrames:
            file_name_local = os.path.splitext(file_name)[0] + '-' + UUIDUtil.get_uuid() + '.jpg'
            cv2.imwrite(file_name_local, image)
        return hasFrames, file_name_local
