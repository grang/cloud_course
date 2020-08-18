# -*- coding: utf-8 -*-
from django.conf import settings

import re
import pytz
import datetime

# 判断是否合法电话
def is_phone(phone):
    if not phone or phone == "":
        return False

    p2 = re.compile(r'^0\d{2,3,5}\d{7,8,9}$|^1[3456789]\d{9}$|^147\d{8}')
    phonematch = p2.match(phone)
 
    if phonematch:
        return True
    else:
        return False

def get_datetime_without_sec(origin_date):
    if not origin_date:
        return ""

    tz = pytz.timezone(settings.TIME_ZONE)
    date = origin_date.astimezone(tz)
    return date.strftime("%Y-%m-%d %H:%M")

def strp_date(value):
    if value == "":
        return ""

    return datetime.datetime.strptime(value, '%Y-%m-%d')