from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    avatar = models.CharField(verbose_name="Аватарка пользователя", max_length=255)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)


