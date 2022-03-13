from django.urls import re_path
from . import views

urlpatterns = [
    re_path('get-system-data', views.get_system_data),
    re_path('get-battery-cell-data', views.get_battery_cell_data),
    re_path('get-system-history-info', views.get_history_system_info),
]