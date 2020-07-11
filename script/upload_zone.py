# -*- coding: utf-8 -*-
import init_django

import traceback

from django.conf import settings
import pandas as pd

from apps.zone.models import Province, City, Area

provincePath = "%s/provinces.csv" % settings.FILE_ROOT
cityPath = "%s/cities.csv" % settings.FILE_ROOT
areaPath = "%s/areas.csv" % settings.FILE_ROOT

provinceDf = pd.read_csv(provincePath)
cityDf = pd.read_csv(cityPath)
areaDf = pd.read_csv(areaPath)

def upload_province(df):
    code = df['code']
    name = df['name']

    try:
        p = Province(code=code, name=name)
        p.save()
    except Exception as e:
       print(traceback.format_exc())

    return df

provinceDf.apply(upload_province, axis=1)

def upload_city(df):
    code = df['code']
    name = df['namee']
    provinceCode = df['provinceCode']

    try:
        p = Province.objects.get(code=provinceCode)

        c = City(code=code, name=name, province=p)
        c.save() 
    except Exception as e:
        print(traceback.format_exc())

    return df

cityDf.apply(upload_city, axis=1)

def upload_area(df):
    code = df['code']
    name = df['name']
    cityCode = df['cityCode']
    provinceCode = df['provinceCode']

    try:
        p = Province.objects.get(code=provinceCode)
        c = City.objects.get(code=cityCode)

        a = Area(code=code, name=name, province=p, city=c)
        a.save()

    except Exception as e:
        print(traceback.format_exc())

    return df
areaDf.apply(upload_area, axis=1)