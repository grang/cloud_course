# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

from apps.course.models import Package
from apps.institution.models import InstTeacher, InstStudent, Institution

class Classroom(models.Model):
    GRADE_ONE, GRADE_TWO, GRADE_THREE, GRADE_FOUR, GRADE_FIVE, GRADE_SIX = range(6)
    GRADE_LIST = [
        (GRADE_ONE, '1年级'),
        (GRADE_TWO, '2年级'),
        (GRADE_ONE, '3年级'),
        (GRADE_ONE, '4年级'),
        (GRADE_ONE, '5年级'),
        (GRADE_ONE, '6年级')
    ]

    name = models.CharField(max_length=127, unique=True, verbose_name="名称")
    grade = models.PositiveSmallIntegerField(default=0, verbose_name="年级", choices=GRADE_LIST)
    institution = models.ForeignKey(Institution, verbose_name="机构", on_delete=models.CASCADE, null=True)

    packages = models.ManyToManyField(Package, verbose_name="所上课程")
    master_teacher = models.ForeignKey(InstTeacher, verbose_name="班主任", on_delete=models.SET_NULL, related_name="master_teacher", blank=True, null=True)
    slave_teacher = models.ManyToManyField(InstTeacher, verbose_name="辅助老师", related_name="slave_teacher")

    students = models.ManyToManyField(InstStudent, verbose_name="学生")

    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"班级"
        verbose_name_plural = verbose_name

        unique_together = ['name', 'grade', 'institution']