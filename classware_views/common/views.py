# coding=utf-8
import datetime
import logging
import traceback


from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.decorators import method_decorator

from lib.decorators import login_required
from apps.classware.models import ClasswareUser

logger = logging.getLogger(__name__)

class CurUserView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        result = {
            'response': 'ok',
            'user': {},
        }
        try:
            user_id = request.session.get('USER_ID')
            if user_id:
                user = ClasswareUser.objects.get(id=user_id)
                if user:
                    if user.is_expired():
                        result['response'] = 'expired'
                    
                    else:
                        result['user'] = user.to_json()
        except:
            logger.error(traceback.format_exc())
        
        return JsonResponse(result)


class MyMenuView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        result = {
            'response': 'ok',
            'menu': [],
        }
        try:
            user_id = request.session.get('USER_ID')
            if user_id:
                user = ClasswareUser.objects.get(id=user_id)
                if user:
                    result['menu'] = user.menu_json()
        except:
            logger.error(traceback.format_exc())
        
        return JsonResponse(result)
    
    
    