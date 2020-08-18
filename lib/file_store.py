# coding=utf-8
import logging
import traceback
import os
import oss2

#import init_django
#from online_course_server import settings
from django.conf import settings

logger = logging.getLogger(__name__)

CONTENT_TYPE = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.csv': 'text/csv',
    '.tar': 'x-tar'
}

bucket = oss2.Bucket(oss2.Auth(settings.ALI_ROOT_ACCESS_KEY, settings.ALI_ROOT_ACCESS_SECRECT), settings.ALI_OSS_ENDPOINT, settings.OSS_BUCKET)


def oss_save_file(file_name, content):
    logger.info('task save file start, file name: %s' % file_name)
    try:
        headers = {
            #'Cache-Control': 'public, max-age=8640000'
        }
        file_ext = os.path.splitext(file_name)[1].lower()
        content_type = CONTENT_TYPE[file_ext] if file_ext in CONTENT_TYPE else ''
        if content_type:
            headers['Content-Type'] = content_type
        
        result = bucket.put_object(file_name, content)
#         logger.error('%s %s' % (result.resp.status, result.request_id))
    except Exception as e:
        logger.error(traceback.format_exc(e))
    logger.info('task save file end\n')


def oss_get_file(file_name):
    try:
        result = bucket.get_object(file_name)
        return result
    except Exception as e:
        logger.error(traceback.format_exc(e))
    return ''
    
def oss_delete_file(file_name):
    try:
        if not file_name:
            return
        bucket.delete_object(file_name)
    except Exception as e:
        logger.error(traceback.format_exc(e))

def oss_load_object_to_file(file_name, to_file_name):
    try:
        bucket.get_object_to_file(file_name, to_file_name)
    except Exception as e:
        logger.error(traceback.format_exc(e))
def load_object_to_file(file_name, to_file_name):
    bucket.get_object_to_file(file_name, to_file_name)


if __name__ == "__main__":
    file_name = '/Users/mac/test.txt'
    xls_obj = open(file_name, 'rb')
    content = xls_obj.read()
    xls_obj.close()
    
    file_name = 'test.txt'
    # 上传一段字符串
    response = oss_save_file(file_name, content)
    
    
    
    
    
    
    
    
    
    
