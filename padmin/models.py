from django.db import models
from django.utils import timezone


# Create your models here.

# 访问网站的 ip 地址、端点和次数
class UserIP(models.Model):
    account = models.CharField(verbose_name='Account', max_length=32)
    ip = models.CharField(verbose_name='IP Address', max_length=30)
    ip_addr = models.CharField(verbose_name='IP Geographical Address', max_length=30)
    character = models.CharField(verbose_name='Character', max_length=32)

    class Meta:
        verbose_name = 'Visit User Information'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip + " ( " + self.account + ", " + self.character + " ）"


class DayNumber(models.Model):
    day = models.DateField(verbose_name='日期', default=timezone.now)
    user = models.ForeignKey(UserIP, verbose_name='userIP', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='visit Num', default=0)  # 网站访问总次数

    class Meta:
        verbose_name = 'User daily visit Num'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.day)
