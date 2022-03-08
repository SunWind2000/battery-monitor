import json

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from . import models


@require_http_methods(['GET'])
def get_system_data(request):
    """
    :param request:
    :return: JSON data
    """
    response = {}
    if request.method == 'GET':
        try:
            last_data_id = models.System.objects.count()
            if last_data_id:
                week_data = models.System.objects.filter(id__lt=last_data_id+1, id__gt=last_data_id-7)
                if week_data:
                    data = json.loads(serializers.serialize('json', week_data))
                    response['status'] = 'success'
                    response['error_msg'] = ''
                    response['data'] = data
                else:
                    response['status'] = 'failure'
                    response['error_msg'] = '数据库检索错误'
                    response['data'] = None
        except Exception as e:
            response['status'] = 'error'
            response['error_msg'] = str(e)
            response['data'] = None
        return JsonResponse(response)


@require_http_methods(['GET'])
def get_battery_cell_data(request):
    """
    :param request: GET
    :return: JSON response
    """
    response = {}
    if request.method == 'GET':
        battery_id = request.GET.get('batteryId')
        try:
            battery_num = models.Battery.objects.filter(battery_id=battery_id).count()
            if battery_num:
                week_data = models.Battery.objects.filter(
                    battery_id=battery_id,
                    id__lt=battery_num + 1,
                    id__gt=battery_num - 7,
                )
                if week_data:
                    response['status'] = 'success'
                    response['error_msg'] = ''
                    response['data'] = json.loads(serializers.serialize('json', week_data))
                else:
                    response['status'] = 'failure'
                    response['error_msg'] = '数据库检索错误'
                    response['data'] = None
        except Exception as e:
            response['status'] = 'error'
            response['error_msg'] = str(e)
            response['data'] = None
        return JsonResponse(response)