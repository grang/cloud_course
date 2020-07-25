#-*- coding: utf-8 -*-
from django.contrib import admin, messages
from django.conf import settings

import traceback

from django.contrib.auth.models import Group
from .models import *

import logging
logger = logging.getLogger(__name__)

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'sales'
    ]

    search_fields = [
        'title'
    ]

    readonly_fields = [
        'sales',
        'dispatch_date',
        'creator',
        'create_date'
    ]

    def get_queryset(self, request):
        qs = super(admin.ModelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(sales__user=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user

        obj.save()

@admin.register(InstManager)
class InstManagerAdmin(admin.ModelAdmin):
    readonly_fields = [
        'creator',
        'create_date'
    ]

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user

        obj.save()

        try:
            group = Group.objects.get(name='机构管理')
            if obj.manager.user:
                # if not group in obj.manager.user.groups:
                obj.manager.user.groups.add(group)
            else:
                messages.error(request, "机构管理员账号还未建立！")
        except Exception as e:
            logger.error(traceback.format_exc())
            messages.error(request, "保存机构管理员权限出错！")

@admin.register(InstConcat)
class InstConcatAdmin(admin.ModelAdmin):
    readonly_fields = [
        'creator',
        'create_date'
    ]

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
            
        obj.save()


@admin.register(InstTeacher)
class InstTeacherAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'institution',
        'teacher'
    ]

    readonly_fields = [
        'creator',
        'create_date'
    ]

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
            
        obj.save()

@admin.register(InstStudent)
class InstStudentAdmin(admin.ModelAdmin):
    readonly_fields = [
        'creator',
        'create_date'
    ]

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
            
        obj.save()

@admin.register(InstCourse)
class InstCourseAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'institution',
        'package',
        'enable',
        'actived_date',
        'expired_date',
    ]
    
    readonly_fields = [
        'creator',
        'create_date'
    ]

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
            
        obj.save()
