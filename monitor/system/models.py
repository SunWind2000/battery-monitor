from django.db import models


# 系统数据表
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


# 单体电池数据表
class Battery(models.Model):
    # 日期时间
    datetime = models.DateTimeField(auto_now_add=False, auto_now=False)
    # 电池编号
    battery_id = models.IntegerField()
    # cell电压数据
    cell_1 = models.FloatField(default=12.6)
    cell_2 = models.FloatField(default=12.6)
    cell_3 = models.FloatField(default=12.6)
    cell_4 = models.FloatField(default=12.6)
    cell_5 = models.FloatField(default=12.6)
    cell_6 = models.FloatField(default=12.6)
    cell_7 = models.FloatField(default=12.6)
    cell_8 = models.FloatField(default=12.6)
    cell_9 = models.FloatField(default=12.6)
    cell_10 = models.FloatField(default=12.6)
    cell_11 = models.FloatField(default=12.6)
    cell_12 = models.FloatField(default=12.6)
    cell_13 = models.FloatField(default=12.6)
    cell_14 = models.FloatField(default=12.6)
    cell_15 = models.FloatField(default=12.6)
    cell_16 = models.FloatField(default=12.6)
    cell_17 = models.FloatField(default=12.6)
    cell_18 = models.FloatField(default=12.6)
    cell_19 = models.FloatField(default=12.6)
    cell_20 = models.FloatField(default=12.6)
    cell_21 = models.FloatField(default=12.6)
    cell_22 = models.FloatField(default=12.6)
    cell_23 = models.FloatField(default=12.6)
    cell_24 = models.FloatField(default=12.6)
    # cell最低最高温度
    max_cell_tem = models.FloatField(default=25.4)
    min_cell_tem = models.FloatField(default=2.5)
    # cell最低最高电压
    max_cell_vol = models.FloatField(default=3.3)
    min_cell_vol = models.FloatField(default=2.4)
    # cell最低最高端电流
    max_cell_cur = models.FloatField(default=0.5)
    min_cell_cur = models.FloatField(default=0.2)
    # cell soc,soh数据
    cell_soc = models.FloatField(default=22.6)
    cell_soh = models.FloatField(default=0.963)

