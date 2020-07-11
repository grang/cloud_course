# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

from django.contrib.auth.models import User

from apps.course.models import Package
from apps.role.models import Manager, Contact, Teacher, Student, Sales 

# 机构
class Institution(models.Model):
    title = models.CharField(max_length=127, unique=True, verbose_name="名称")

    address = models.CharField(max_length=255, verbose_name="机构地址", default="")
    remark = models.TextField(default="", verbose_name="备注", null=True, blank=True)

    sales = models.ForeignKey(Sales, verbose_name="分配的销售", null=True, blank=True, on_delete=models.CASCADE)
    dispatch_date = models.DateTimeField(verbose_name="分配时间", null=True, blank=True)

    creator = models.ForeignKey(User, verbose_name="建立者", blank=True, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"机构"
        verbose_name_plural = verbose_name

class InstManager(models.Model):
    institution = models.ForeignKey(Institution, verbose_name="对应机构", on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, verbose_name="对应管理员", on_delete=models.CASCADE)

    creator = models.ForeignKey(User, verbose_name="建立者", blank=True, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return "%s %s" % (self.institution.__str__(), self.manager.__str__())

    class Meta:
        verbose_name = u"机构管理员"
        verbose_name_plural = verbose_name

        unique_together = ['institution', 'manager']

class InstConcat(models.Model):
    institution = models.ForeignKey(Institution, verbose_name="对应机构", on_delete=models.CASCADE)
    concat = models.ForeignKey(Contact, verbose_name="对应联系人", on_delete=models.CASCADE)

    creator = models.ForeignKey(User, verbose_name="建立者", blank=True, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return "%s %s" % (self.institution.__str__(), self.concat.__str__())

    class Meta:
        verbose_name = u"机构联系人"
        verbose_name_plural = verbose_name

        unique_together = ['institution', 'concat']

class InstTeacher(models.Model):
    institution = models.ForeignKey(Institution, verbose_name="对应机构", on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, verbose_name="对应老师", on_delete=models.CASCADE)

    creator = models.ForeignKey(User, verbose_name="建立者", blank=True, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return "%s %s" % (self.institution.__str__(), self.teacher.__str__())

    class Meta:
        verbose_name = u"机构老师"
        verbose_name_plural = verbose_name

        unique_together = ['institution', 'teacher']

class InstStudent(models.Model):
    institution = models.ForeignKey(Institution, verbose_name="对应机构", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name="对应学生", on_delete=models.CASCADE)

    creator = models.ForeignKey(User, verbose_name="建立者", blank=True, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return "%s %s" % (self.institution.__str__(), self.student.__str__())

    class Meta:
        verbose_name = u"机构学生"
        verbose_name_plural = verbose_name

        unique_together = ['institution', 'student']

class InstCourse(models.Model):
    institution = models.ForeignKey(Institution, verbose_name="对应机构", on_delete=models.CASCADE)
    package = models.ForeignKey(Package, verbose_name="机构解锁的课程", on_delete=models.CASCADE)

    enabel = models.BooleanField(default=False, verbose_name="是否可以使用课程")

    expired_date = models.DateField(verbose_name="过期时间", null=True, blank=True)
    actived_date = models.DateField(verbose_name="激活时间", null=True, blank=True)

    creator = models.ForeignKey(User, verbose_name="建立者", blank=True, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return "%s %s" % (self.institution.__str__(), self.package.__str__())

    class Meta:
        verbose_name = u"机构课程"
        verbose_name_plural = verbose_name

        unique_together = ['institution', 'package']