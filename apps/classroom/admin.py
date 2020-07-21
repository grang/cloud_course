#-*- coding: utf-8 -*-
from django.contrib import admin, messages
from django.conf import settings

from .models import *

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'institution', 'teacher']
    list_filter = ["institution"]

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ["id", "classroom", "ware", "title", "finish_date", "create_date", "showInst"]
    list_filter = ["ware__package"]

    def showInst(self, obj):
        return obj.getInstName()
    showInst.short_description = u"所属机构"

@admin.register(StudentHomework)    
class StudentHomeworkAdmin(admin.ModelAdmin):
    list_display = ["id", "homework", "student", "content", "is_upload", "upload_date", "showInst"]
    list_filter = ["is_upload"]

    def showInst(self, obj):
        return obj.homework.getInstName()
    showInst.short_description = u"所属机构"