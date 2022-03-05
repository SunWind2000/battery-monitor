from django.urls import re_path
from . import views

urlpatterns = [
    re_path('login', views.login),
    re_path('update-user-data', views.update_user_data),
    re_path('update-user-password', views.update_user_pwd),
    re_path(r'upload-user-avatar/$', views.upload_user_avatar),
]
