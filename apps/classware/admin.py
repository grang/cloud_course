#-*- coding: utf-8 -*-
import logging
import traceback

from django.contrib import admin, messages
from django.conf import settings

import traceback

from .models import *

import logging
logger = logging.getLogger(__name__)

@admin.register(ClasswareUser)
class ClasswareUserAdmin(admin.ModelAdmin):
    pass
