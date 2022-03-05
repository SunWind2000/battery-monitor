from django.urls import re_path
from . import views

urlpatterns = [
    re_path('get-system-data', views.get_system_data),
]