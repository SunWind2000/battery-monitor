from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=40, unique=True)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=6)
    avatar = models.ImageField(upload_to='avatar/', default=None)
