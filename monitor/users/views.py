from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from . import models
import json


@require_http_methods(['GET'])
def login(request):
    """
    :param: request
    :return: JSON data
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
                response['error_msg'] = '用户名或密码错误，请重试'
                response['data'] = None
        except Exception as e:
            response['status'] = 'error'
            response['error_msg'] = str(e)
            response['data'] = None
    return JsonResponse(response)


@require_http_methods(['GET'])
def update_user_data(request):
    """
    :param request: HTTP request
    :return: Json response
    """
    response = {}
    if request.method == 'GET':
        username = request.GET.get('username')
        nickname = request.GET.get('nickname')
        phone = request.GET.get('phone')
        gender = request.GET.get('gender')
        email = request.GET.get('email')
        data = {
            "username": username,
            "nickname": nickname,
            "phone": phone,
            "gender": gender,
            "email": email
        }
        try:
            usr = models.User.objects.filter(username=username)
            if usr:
                models.User.objects.filter(
                    username=username
                ).update(
                    nickname=nickname,
                    phone=phone,
                    gender=gender,
                    email=email
                )
                response['status'] = 'success'
                response['error_msg'] = ''
                response['data'] = data
            else:
                response['status'] = 'failure'
                response['error_msg'] = '用户不存在'
                response['data'] = data
        except Exception as e:
            response['status'] = 'error'
            response['error_msg'] = str(e)
            response['data'] = data
    return JsonResponse(response)


@require_http_methods(['GET'])
def update_user_pwd(request):
    """
    :param request: HTTP request
    :return: JSON response
    """
    response = {}
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        data = {
            "username": username,
            "password": password
        }
        try:
            usr = models.User.objects.filter(username=username)
            if usr:
                models.User.objects.filter(
                    username=username
                ).update(
                    password=password
                )
                response['status'] = 'success'
                response['error_msg'] = ''
                response['data'] = data
            else:
                response['status'] = 'failure'
                response['error_msg'] = '用户不存在'
                response['data'] = data
        except Exception as e:
            response['status'] = 'error'
            response['error_msg'] = str(e)
            response['data'] = data
    return JsonResponse(response)
