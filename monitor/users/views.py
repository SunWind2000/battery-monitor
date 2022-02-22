from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from . import models
import json


@require_http_methods(['GET'])
def login(request):
    """
    Name: login
    param: request
    description: User login view function,using auth to complete login verification
    return: JSON data
    """
    response = {}
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        try:
            usr = models.User.objects.filter(username=username, password=password)
            if usr:
                response['status'] = 'success'
                response['error_msg'] = ''
                response['data'] = json.loads(serializers.serialize('json', usr))
            else:
                response['status'] = 'failure'
                response['error_msg'] = '用户名或密码错误?'+'username='+str(username)+'&'+'password='+str(password)
                response['data'] = None
        except Exception as e:
            response['status'] = 'error'
            response['error_msg'] = str(e)
            response['data'] = None
    return JsonResponse(response)
