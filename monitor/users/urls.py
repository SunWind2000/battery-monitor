from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('login', views.login),
    re_path('update-user-data', views.update_user_data),
    re_path('update-user-password', views.update_user_pwd),
]
