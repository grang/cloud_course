# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

class Province(models.Model):
    code = models.CharField(max_length=64, verbose_name="编码", unique=True)
    name = models.CharField(max_length=255, verbose_name="名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"省"
        verbose_name_plural = verbose_name

class City(models.Model):
    code = models.CharField(max_length=64, verbose_name="编码", unique=True)
    name = models.CharField(max_length=255, verbose_name="名称")
    province = models.ForeignKey(Province, verbose_name="省", on_delete=models.CASCADE)

    def __str__(self):
        return "%s%s" % (self.province.name, self.name)

    class Meta:
        verbose_name = u"市"
        verbose_name_plural = verbose_name

class Area(models.Model):
    code = models.CharField(max_length=64, verbose_name="编码", unique=True)
    name = models.CharField(max_length=255, verbose_name="名称")

    province = models.ForeignKey(Province, verbose_name="省", on_delete=models.CASCADE)
    city = models.ForeignKey(City, verbose_name="市", on_delete=models.CASCADE)

    def __str__(self):
        return "%s%s%s" % (self.province.name, self.city.name, self.name)

    class Meta:
        verbose_name = u"区"
        verbose_name_plural = verbose_name

