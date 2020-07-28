#-*- coding: utf-8 -*-
from django.contrib import admin, messages
from django.conf import settings

from django.utils.safestring import mark_safe

from .models import Material, Package, Ware

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):    
    list_display = [
        "id",
        "title",
        "types",
        "show_view"
    ]

    search_fields = [
        "title"
    ]

    list_filter = [
        'types'
    ]

    def show_view(self, obj):
        return mark_safe("<a href='%s' target='_blank'>查看</a>" % obj.url)
    show_view.short_description = u"查看"

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'count',
        'grade'
    ]

    list_filter = ['grade']

@admin.register(Ware)
class WareAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'intro',
        'package',
        'index'
    ]

    list_filter = ['package']
