from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.hashers import make_password


# Create your models here.
def validate_pwd(pwd):
    if len(pwd) < 6:
        raise ValidationError(
            _('%(pwd)s must be at least 6 characters'),
            params={'pwd': pwd},
        )




class Student(models.Model):
    account = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256, validators=[validate_pwd])
    email = models.EmailField()

    password_en = models.BooleanField(default=False)
    encrypt_items = ['password']

    def save(self, *args, **kwargs):
        for attr in self.encrypt_items:
            if not getattr(self, '%s_en' % attr):
                self.__setattr__(attr, make_password(getattr(self, attr)))
                self.__setattr__('%s_en' % attr, True)
        super(Student, self).save(*args, **kwargs)

    class Meta:
        db_table = "Student"

    def __str__(self):
        return self.account


class Student_Information(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    grade = models.CharField(max_length=10, default=timezone.now().year)
    sex = models.CharField(max_length=5, default='男')
    education = models.CharField(max_length=10, default='本科')
    school = models.CharField(max_length=50, default='南方科技大学')
    major = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "Student_Information"
