#-*- coding: utf-8 -*-
from django.contrib import admin, messages
from django.conf import settings

from .models import *

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    pass

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    pass