from django.db import models


class CpuData(models.Model):
    cpu_utilization = models.IntegerField(verbose_name='Утилизация ЦП, %')
