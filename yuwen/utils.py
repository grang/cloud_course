# -*- coding: utf-8 -*-
import re

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