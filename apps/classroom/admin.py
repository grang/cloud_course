#-*- coding: utf-8 -*-
from django.contrib import admin, messages
from django.conf import settings

from .models import *

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    pass