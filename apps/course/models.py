# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

# 课程材料
class Material(models.Model):
    PDF_TYPE, MP4_TYPE, IMG_TYPE, DOC_TYPE, EXCEL_TYPE, URL_TYPE, PPT_TYPE = range(7)

    TYPE_LIST = [
        (PDF_TYPE, 'pdf'),
        (MP4_TYPE, 'mp4'),
        (IMG_TYPE, '图片'),
        (DOC_TYPE, 'DOC'),
        (EXCEL_TYPE, 'Excel'),
        (URL_TYPE, 'html'),
        (PPT_TYPE, 'ppt')
    ]

    title = models.CharField(max_length=127, unique=True, verbose_name="名称")
    types = models.PositiveSmallIntegerField(default=0, choices=TYPE_LIST, verbose_name="类型")
    url = models.URLField(default="", verbose_name="地址链接", blank=True)
    path = models.CharField(max_length=127, verbose_name="地址", blank=True, default="")
    is_teacher_user = models.BooleanField(default=False, verbose_name="是否教师使用")

    def toDict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'type': self.TYPE_LIST[self.types][1]
        }

    def __str__(self):
        return self.title

    def getType(self):
        return Material.TYPE_LIST[self.types][1]

    def isPPT(self):
        if self.types == self.PPT_TYPE:
            return True
        return False
    
    class Meta:
        verbose_name = u"资料"
        verbose_name_plural = verbose_name

# 课程
class Package(models.Model):
    GRADE_ONE, GRADE_TWO, GRADE_THREE, GRADE_FOUR, GRADE_FIVE, GRADE_SIX = range(6)
    GRADE_LIST = [
        (GRADE_ONE, '1年级'),
        (GRADE_TWO, '2年级'),
        (GRADE_ONE, '3年级'),
        (GRADE_ONE, '4年级'),
        (GRADE_ONE, '5年级'),
        (GRADE_ONE, '6年级')
    ]

    SPRING, SUMMER, AUTOMER, WINTER = range(4)
    SEASON_LIST = [
        (SPRING, '春季'),
        (SUMMER, '夏季'),
        (AUTOMER, '秋季'),
        (WINTER, '冬季')
    ]

    title = models.CharField(max_length=127, verbose_name="课程名称", unique=True)
    intro = models.TextField(default="", verbose_name="课程介绍", blank=True)

    count = models.PositiveSmallIntegerField(default=0, verbose_name="课节数", blank=True)

    cover_img = models.URLField(default="", verbose_name="封面图片", blank=True)
    thum_img = models.URLField(default="", verbose_name="缩略图", blank=True)

    season = models.PositiveSmallIntegerField(default=0, verbose_name="适用季节", choices=SEASON_LIST)
    grade = models.PositiveSmallIntegerField(default=0, verbose_name="适用年级", choices=GRADE_LIST)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

class Ware(models.Model):
    title = models.CharField(max_length=127, verbose_name="课节名称")
    intro = models.TextField(default="", verbose_name="课节介绍", blank=True)
    package = models.ForeignKey(Package, verbose_name="所属课程", on_delete=models.CASCADE)
    index = models.PositiveSmallIntegerField(default=0, verbose_name="课序号")

    # 封面图片地址
    cover = models.URLField(default="", verbose_name="封面图片", blank=True)
    thum_img = models.URLField(default="", verbose_name="缩略图", blank=True)

    material = models.ManyToManyField(Material, verbose_name="课节资料")

    def __str__(self):
        return "%s 第%d节课 %s" % (self.package.title, self.index, self.title)

    class Meta:
        verbose_name = "课节"
        verbose_name_plural = verbose_name

        unique_together = ['package', 'title']