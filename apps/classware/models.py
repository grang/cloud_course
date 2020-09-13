#-*- coding: utf-8 -*-
import hashlib
import ujson
import datetime
from django.db import models


# 云课系统web版用户
class ClasswareUser(models.Model):
    username = models.CharField(max_length=64, verbose_name="用户名", unique=True)
    password = models.CharField(max_length=64, verbose_name="密码", default="")
    expire_date = models.DateField(null=True, blank=True, verbose_name="过期时间")
    menu = models.TextField(default="", null=True, blank=True, verbose_name="所属菜单")

    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return "%s" % (self.username)

    class Meta:
        verbose_name = "云课系统web账号"
    
    @staticmethod
    def encrypt_password(pwd):
        return hashlib.sha1(pwd.encode('utf-8')).hexdigest()
    
    def set_password(self, password):
        self.password = self.encrypt_password(password)
    
    def check_password(self, password):
        return self.password == self.encrypt_password(password)
    
    def is_expired(self):
        _is_expired = False
        now = datetime.datetime.now()
        now = datetime.date(now.year, now.month, now.day)
        if self.expire_date and self.expire_date < now:
            _is_expired = True
        return _is_expired
    
    def menu_json(self):
        menu = []
        try:
            menu = ujson.loads(self.menu)
        except:
            pass
        return menu
    
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'menu_list': self.menu_json(),
            'expire_date': self.expire_date,
        }
