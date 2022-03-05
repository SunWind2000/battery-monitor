from django.db import models


# 系统数据库
class System(models.Model):
    datetime = models.CharField(max_length=20, unique=True)
    max_voltage = models.FloatField(default=0.0)
    min_voltage = models.FloatField(default=0.0)
    total_voltage = models.FloatField(default=0.0)
    max_current = models.FloatField(default=0.0)
    min_current = models.FloatField(default=0.0)
    soc = models.FloatField(default=0.0)
    max_temperature = models.FloatField(default=0.0)
    min_temperature = models.FloatField(default=0.0)
    battery_num = models.IntegerField(default=0)
