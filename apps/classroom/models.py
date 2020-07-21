# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

from apps.course.models import Package, Ware
from apps.institution.models import InstTeacher, InstStudent, Institution, InstCourse

from yuwen.utils import get_datetime_without_sec


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

    title = models.CharField(max_length=127, unique=True, verbose_name="名称")
    grade = models.PositiveSmallIntegerField(default=0, verbose_name="年级", choices=GRADE_LIST)
    institution = models.ForeignKey(Institution, verbose_name="机构", on_delete=models.CASCADE, null=True)

    packages = models.ManyToManyField(Package, verbose_name="所上课程")
    teacher = models.ForeignKey(InstTeacher, verbose_name="班主任", on_delete=models.SET_NULL, related_name="master_teacher", blank=True, null=True)
    # slave_teacher = models.ManyToManyField(InstTeacher, verbose_name="辅助老师", related_name="slave_teacher")

    students = models.ManyToManyField(InstStudent, verbose_name="学生")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def toDict(self):
        return {
            "id": self.id,
            "title": self.title,
            "grade": self.GRADE_LIST[self.grade][1],
            "studentCount": self.students.all().count()
        }
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"班级"
        verbose_name_plural = verbose_name

        unique_together = ['title', 'grade', 'institution']


class Homework(models.Model):
    classroom = models.ForeignKey(Classroom, verbose_name="对应班级", on_delete=models.CASCADE)
    ware = models.ForeignKey(Ware, verbose_name="对应课节", on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=127, verbose_name="作业标题")
    content = models.TextField(default="", verbose_name="作业内容")
    finish_date = models.DateTimeField(verbose_name="作业截止时间")

    img1 = models.URLField(default="", blank=True, verbose_name="作业附图1")
    img2 = models.URLField(default="", blank=True, verbose_name="作业附图2")
    img3 = models.URLField(default="", blank=True, verbose_name="作业附图3")

    voice = models.URLField(default="", blank=True, verbose_name="声音文件")

    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def getInstName(self):
        return self.classroom.institution.title

    def getWareName(self):
        if self.ware:
            return self.ware.title
        return ""

    def __str__(self):
        return self.title
        # return "%s_%s_%s" % (self.title, self.classroom.__str__(), self.course.__str__())

    def toDict(self):
        return {
            'id': self.id,
            'classroomId': self.classroom.id,
            'title': self.title,
            'publishedDate': get_datetime_without_sec(self.create_date),
            'endDate': get_datetime_without_sec(self.finish_date),
        }

    class Meta:
        verbose_name = u"作业"
        verbose_name_plural = verbose_name

class StudentHomework(models.Model):
    homework = models.ForeignKey(Homework, verbose_name="对应的作业", on_delete=models.CASCADE)
    student = models.ForeignKey(InstStudent, verbose_name="学员", on_delete=models.CASCADE)    

    content = models.TextField(default="", verbose_name="提交的文字内容", blank=True)
    img = models.URLField(default="", blank=True, verbose_name="作业附图")

    voice = models.URLField(default="", blank=True, verbose_name="声音文件")
    is_upload = models.BooleanField(default=False, verbose_name="是否提交", blank=True)
    upload_date = models.DateTimeField(null=True, blank=True, verbose_name="提交时间")

    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    # judge info
    is_judge = models.BooleanField(default=False, verbose_name="是否点评")
    judge_date = models.DateTimeField(verbose_name="点评时间", blank=True, null=True)
    judge_voice = models.URLField(default="", verbose_name="点评语音", blank=True)

    def toDict(self):
        return {
            'id': self.id,
            'title': self.homework.title,
            'classroomId': self.homework.classroom.id,
            'courseName': self.homework.getWareName(),
            'publishedDate': get_datetime_without_sec(self.homework.create_date),
            'endDate': get_datetime_without_sec(self.homework.finish_date)
        }
    
    class Meta:
        verbose_name = u"学生提交作业"
        verbose_name_plural = verbose_name

        unique_together = ['homework', 'student']