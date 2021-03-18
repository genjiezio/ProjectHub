from django.db import models
from django.contrib.auth.hashers import make_password


# Create your models here.

class Teacher(models.Model):
    account = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64)
    password_en = models.BooleanField(default=False)
    encrypt_items = ['password']

    def save(self, *args, **kwargs):
        for attr in self.encrypt_items:
            if not getattr(self, '%s_en' % attr):
                self.__setattr__(attr, make_password(getattr(self, attr)))
                self.__setattr__('%s_en' % attr, True)
        # 调用父类Model的save函数，进行真正的数据库插入操作
        super(Teacher, self).save(*args, **kwargs)

    class Meta:
        db_table = "Teacher"

    def __str__(self):
        return self.account