# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

from django.contrib.auth.models import User

class BaseRole(models.Model):
    name = models.CharField(max_length=127, verbose_name="名称")
    phone = models.CharField(max_length=64, verbose_name="电话", unique=True)
    
    creator = models.ForeignKey(User, verbose_name="建立者", blank=True, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Manager(BaseRole):
    email = models.EmailField(verbose_name="对应邮箱", null=True, unique=True)
    user = models.ForeignKey(User, verbose_name="对应账号", blank=True, null=True, on_delete=models.CASCADE, related_name="manager_user")

    class Meta:
        verbose_name = "管理员"
        verbose_name_plural = verbose_name

class Sales(BaseRole):
    email = models.EmailField(verbose_name="对应邮箱", null=True, unique=True)
    user = models.ForeignKey(User, verbose_name="对应账号", blank=True, null=True, on_delete=models.CASCADE, related_name="sales_user")

    class Meta:
        verbose_name = "销售"
        verbose_name_plural = verbose_name


class Contact(BaseRole):

    class Meta:
        verbose_name = "联系人"
        verbose_name_plural = verbose_name

class Teacher(BaseRole):
    head = models.URLField(default="", verbose_name="头像", blank=True)
    openid = models.CharField(max_length=64, verbose_name="openid", default="", blank=True, unique=True)
    unionid = models.CharField(max_length=64, verbose_name="unionid", default="", blank=True)
    wx_session = models.CharField(max_length=64, verbose_name="微信session", default="", blank=True)

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

class Student(BaseRole):
    UNKWON, MALE, FEMALE = range(3)
    GENDER = [
        ('未知', UNKWON),
        ('男性', MALE),
        ('女性', FEMALE)
    ]

    head = models.URLField(default="", verbose_name="头像", blank=True)
    openid = models.CharField(max_length=64, verbose_name="openid", unique=True)
    unionid = models.CharField(max_length=64, verbose_name="unionid", default="", blank=True)
    wx_session = models.CharField(max_length=64, verbose_name="微信session", default="", blank=True)

    gender = models.PositiveSmallIntegerField(default=0, verbose_name="性别", choices=GENDER)
    country = models.CharField(max_length=127, verbose_name="国家", default="", blank=True)
    province = models.CharField(max_length=127, verbose_name="省份", default="", blank=True)
    city = models.CharField(max_length=127, verbose_name="城市", default="", blank=True)

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = verbose_name

