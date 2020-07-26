# -*- coding: utf-8 -*-
import logging
import traceback
import requests
import json

from django.conf import settings

logger = logging.getLogger(__file__)


class WeixinMiniBase(object):
    """
     小程序接口公用类
    """
    _instances = dict()

    code2session_url = 'https://api.weixin.qq.com/sns/jscode2session'

    @staticmethod
    def get_instance(app_id, app_secret):
        instance = WeixinMiniBase._instances.get(app_id + app_secret)
        if instance:
            return instance

        return WeixinMiniBase(app_id, app_secret)

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        WeixinMiniBase._instances[app_id + app_secret] = self

    def get_miniprogram_session(self, code):
        access_token_url = '%s?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (self.code2session_url, self.app_id, self.app_secret, code)
        result = {}
        try:
            req = requests.post(access_token_url)
            result = json.loads(req.content)
            logger.debug('miniprogram_session: %s' % result)
        except:
            logger.error(traceback.format_exc())

        return result