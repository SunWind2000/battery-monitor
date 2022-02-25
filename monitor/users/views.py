import datetime
import json
import os

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from . import models


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


@require_http_methods(['POST'])
def upload_user_avatar(request):
    """
    :param request: HTTP request
    :return: JSON response
    """
    response = {}
    img = request.FILES['userAvatar']
    username = request.POST.get('username')
    new_img_name = username + '-' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.png'
    data = {
        "img_name": 'avatar/' + new_img_name
    }
    try:
        usr = models.User.objects.get(username=username)
        if usr:
            usr.avatar.save(new_img_name, img)
            response['status'] = 'success'
            response['error_msg'] = ''
            response['data'] = data
        else:
            response['status'] = 'failure'
            response['error_msg'] = '头像上传失败'
            response['data'] = data
    except Exception as e:
        response['status'] = 'error'
        response['error_msg'] = str(e)
        response['data'] = data
    return JsonResponse(response)
