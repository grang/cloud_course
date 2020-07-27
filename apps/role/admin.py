#-*- coding: utf-8 -*-
from django.contrib import admin, messages
from django.conf import settings

from django.utils.safestring import mark_safe

from django.contrib.auth.models import User
from .models import *

from yuwen.utils import is_phone

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'phone',
        'email'
    ]

    search_fields = [
        'name',
        'phone',
        'email'
    ]

    readonly_fields = [
        'creator',
        'create_date',
        'user'
    ]

    def save_model(self, request, obj, form, change):
        if is_phone(obj.phone):
            # 建立可以登录的用户账号
            if not obj.user:        
                user = User.objects.create_user(username=obj.phone, email=obj.email, password=settings.DEFAULT_PWD, is_active=True, first_name=obj.name, is_staff=True)
                obj.user = user
                obj.save()

            # 建立创建者信息
            if not obj.creator:
                obj.creator = request.user

            obj.save()

            # TODO: 给于销售的默认权限
        else:
            messages.error(request, "错误：%s 的电话非法，请重新填写" % obj.name)



@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'phone',
        'email'
    ]

    search_fields = [
        'name',
        'phone',
        'email'
    ]

    readonly_fields = [
        'creator',
        'create_date',
        'user'
    ]

    def save_model(self, request, obj, form, change):
        if is_phone(obj.phone):
            # 建立可以登录的用户账号
            if not obj.user:        
                user = User.objects.create_user(username=obj.phone, email=obj.email, password=settings.DEFAULT_PWD, is_active=True, first_name=obj.name, is_staff=True)
                obj.user = user
                obj.save()

            # 建立创建者信息
            if not obj.creator:
                obj.creator = request.user

            obj.save()

            # TODO: 给予管理员的默认权限
        else:
            messages.error(request, "错误：%s 的电话非法，请重新填写" % obj.name)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'phone'
    ]

    readonly_fields = [
        'creator',
        'create_date'
    ]

    def save_model(self, request, obj, form, change):
        if is_phone(obj.phone):
            obj.save()
        else:
            messages.error(request, "错误：%s 的电话非法，请重新填写" % obj.name)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'phone'
    ]

    readonly_fields = [
        'creator',
        'create_date'
    ]

    def save_model(self, request, obj, form, change):
        if is_phone(obj.phone):
            obj.save()
        else:
            messages.error(request, "错误：%s 的电话非法，请重新填写" % obj.name)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'openid',
        'show_head',
        'wx_session',
        'gender',
        'country',
        'province',
        'city'
    ]

    readonly_fields = [
        'name',
        'openid',
        'head',
        'wx_session',
        'gender',
        'country',
        'province',
        'city'

        'creator',
        'create_date'
    ]

    def show_head(self, obj):
        return mark_safe("<img src='%s' width=100 height=100 />" % obj.head)
    show_head.short_description = "头像"
    
    def save_model(self, request, obj, form, change):
        if is_phone(obj.phone):
            obj.save()
        else:
            messages.error(request, "错误：%s 的电话非法，请重新填写" % obj.name)
