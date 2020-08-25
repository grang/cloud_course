# -*- coding: utf-8 -*-
from django.urls import include, path, re_path
from django.views.static import serve
from django.conf import settings

from views.api_views import TestView, ClassroomView, ClassroomNamesView, ClassroomInfoView, ClassroomStudents, StudentHomeworkListView, StudentInfoView, ClasswareListView
from views.api_views import HomeworkView, HomeworkImgUpload, HomeworkUpload
from views.api_views import LoginView, WxPhoneView
from views.api_views import MenuInfoView

urlpatterns = [
    re_path('test/$', TestView.as_view()),

    # 获得班级列表
    re_path('classroom/$', ClassroomView.as_view()),

    # 获得班级信息
    re_path('classroom/info/$', ClassroomInfoView.as_view()),

    # 获得班级课程
    re_path('classroom/course/nams/$', ClassroomNamesView.as_view()),

    # 获得班级下学生列表
    re_path('students/$', ClassroomStudents.as_view()),

    # 获得学生信息
    re_path('student/info/$', StudentInfoView.as_view()),

    # 作业列表
    re_path('homewoks/$', HomeworkView.as_view()),

    # 作业图片上传
    re_path('homework/img/upload/$', HomeworkImgUpload.as_view()),

    # 作业上传
    re_path('homework/upload/$', HomeworkUpload.as_view()),

    # 班级学生的作业列表
    re_path('students_homework_list/$', StudentHomeworkListView.as_view()),

    # 课件列表
    re_path('classwares/$', ClasswareListView.as_view()),

    # 用户登录
    re_path('login/$', LoginView.as_view()),
    # 电话获得
    re_path('wx_phone/$', WxPhoneView.as_view()),

    # 上课用户获得页面
    re_path('menu_info/$', MenuInfoView.as_view())
]