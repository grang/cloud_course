#-*- coding: utf-8 -*-
from django.contrib import admin, messages
from django.conf import settings

from .models import Material, Package, Ware

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):    
    search_fields = ["title"]
    list_filter = ['types']

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_filter = ['grade']

@admin.register(Ware)
class WareAdmin(admin.ModelAdmin):
    list_filter = ['package']
