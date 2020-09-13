#coding=utf-8
import time
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.conf  import settings
        
def _login_required():
    def _dec(view_func):
        def check_login(request, *args, **kwargs):
            
            user_id = request.session.get('USER_ID', None)
            if not user_id:
                http_referer = request.META.get('HTTP_REFERER','')
                if not http_referer:
                    http_referer = request.GET.get('REFERER','')
                    
                is_ajax = request.META.get('HTTP_AJAX','')
                if is_ajax=='ajax' or request.is_ajax():
                    result = {
                        'response': 'NoLogin',
                        'info': u'未登陆，请先登陆'
                    }
                    return JsonResponse(result)  
                return HttpResponse('Nologin')  
            else:
                return view_func(request, *args, **kwargs)
        return check_login
    return _dec
login_required = _login_required()



