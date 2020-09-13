# coding=utf-8
import time
import random
import logging
import traceback

import json

from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse

from apps.classware.models import ClasswareUser

from lib.my_encode import MyEncoder

logger = logging.getLogger(__name__)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        version = time.time() + random.randint(100, 999)
        context['version'] = version
        
        return render(request, 'index.html', context)

    
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        for sesskey in request.session.keys():
            del request.session[sesskey]
            
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def post(self, request, *args, **kwargs):
        result = {'response':'ok', 'info': '', 'user': {}}
        
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        try:
            user = ClasswareUser.objects.filter(username=username).first()

            if not user or not user.password == password:
                result.update(response='fail', info='用户名或密码错误')
                return JsonResponse(result)
            
            if user.is_expired():
                result.update(response='expired', info='已过期')
                return JsonResponse(result)
            
            request.session['USER_ID'] = user.id
            
            result.update(user=user.to_json())
        except Exception as e:
            print(e)

            result.update(response='fail', info='用户名或密码错误')
        finally:
            return JsonResponse(result)      
        