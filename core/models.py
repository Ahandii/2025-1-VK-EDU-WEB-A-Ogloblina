
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
    avatar = models.ImageField(verbose_name="Аватарка пользователя (сжатая)", max_length=255, upload_to='avatars/')
    original_avatar = models.ImageField(verbose_name="Аватарка пользователя", max_length=255, upload_to='originalavatars/', default='')
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id}"
    
    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        if self.original_avatar:
            return self.original_avatar.url
        return "/static/avatars/no-avatar.jpeg" 