#coding:utf-8
from django.urls import include, path, re_path
from django.views.static import serve
from django.conf import settings

from classware_views.index.views import IndexView, LoginView, LogoutView
from classware_views.common.views import CurUserView, MyMenuView


urlpatterns = [
    re_path('static/(?P<path>.*)$', serve, { 'document_root': settings.STATIC_PATH}),

    
    re_path('^$', IndexView.as_view(), name='index'),
    re_path('^login/$', LoginView.as_view()),
    re_path('^logout/$', LogoutView.as_view()),
    
    re_path('^common/curuser/$', CurUserView.as_view()),
    re_path('^common/menu/$', MyMenuView.as_view()),
]





