from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    title =  models.CharField(verbose_name="Вопрос", max_length=255)
    content = models.CharField(verbose_name="Текст вопроса", max_length=255)
    author = models.ForeignKey(User, verbose_name="Автора вопроса", on_delete=models.SET_NULL, null=True)

    likes = models.IntegerField(verbose_name="Количество лайков")

    created_at = models.DateTimeField(verbose_name="Время создания вопроса", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name="Время редактирования вопроса", auto_now=True)

class Answer(models.Model):
    content = models.CharField(verbose_name="Текст вопроса", max_length=255)
    author = models.ForeignKey(User, verbose_name="Автора вопроса", on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey("questions.Question", verbose_name = "Вопрос", on_delete=models.CASCADE)

    likes = models.IntegerField(verbose_name="Количество лайков")

    created_at = models.DateTimeField(verbose_name="Время создания вопроса", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name="Время редактирования вопроса", auto_now=True)

class QuestionLikes(models.Model):
    question = models.ForeignKey("questions.Question", verbose_name = "Вопрос", on_delete=models.CASCADE)
    
    