from django.db import models
from django.contrib.auth.models import User
from questions.managers import QuestionManager, AnswerManager, TagManager

class Profile(models.Model):
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
    avatar = models.CharField(verbose_name="Аватарка пользователя", max_length=255)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f"{self.user}"
    
class Tag(models.Model):
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
    name = models.CharField(verbose_name="Название тега", max_length=255, unique=True)
    def __str__(self):
        return f"Тег {self.name}"
    objects = TagManager()
    
class Question(models.Model):
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    title =  models.CharField(verbose_name="Вопрос", max_length=255)
    content = models.CharField(verbose_name="Текст вопроса", max_length=255)
    author = models.ForeignKey(User, verbose_name="Автор вопроса", on_delete=models.SET_NULL, null=True)

    likes = models.IntegerField(verbose_name="Количество лайков", default=0)

    created_at = models.DateTimeField(verbose_name="Время создания вопроса", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name="Время редактирования вопроса", auto_now=True)

    answers_cnt = models.IntegerField(verbose_name = "Количество ответов", default = 0)
    
    is_active = models.BooleanField(verbose_name = "Активно?", help_text="true - отобразится пользователям", default = True)

    tags = models.ManyToManyField(Tag, verbose_name = "Теги", blank=True)

    def __str__(self):
        return f"Вопрос #{self.id} {self.title}"
    
    objects = QuestionManager()
    
class Answer(models.Model):
    class Meta:
        verbose_name = "Ответ на вопрос"
        verbose_name_plural = "Ответы на вопросы"
    content = models.CharField(verbose_name="Текст ответа", max_length=255)
    author = models.ForeignKey(User, verbose_name="Автор ответа", on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey("questions.Question", verbose_name = "Вопрос", on_delete=models.CASCADE)

    likes = models.IntegerField(verbose_name="Количество лайков", default = 0)

    created_at = models.DateTimeField(verbose_name="Время создания вопроса", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name="Время редактирования вопроса", auto_now=True)

    is_active = models.BooleanField(verbose_name = "Активно?", help_text="true - отобразится пользователям", default = True)
    is_correct = models.BooleanField(verbose_name = "Правильный ответ?", help_text="true - правильный", default = False)
    
    def __str__(self):
        return f"Ответ #{self.id}"
    
    objects = AnswerManager()
    
class QuestionLikes(models.Model):
    class Meta:
        verbose_name = "Лайк к вопросу"
        verbose_name_plural = "Лайки к вопросам"
        unique_together = ['user', 'question']
    question = models.ForeignKey("questions.Question", verbose_name = "Вопрос", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

class AnswerLikes(models.Model):
    class Meta:
        verbose_name = "Лайк к ответу"
        verbose_name_plural = "Лайки к ответам"
        unique_together = ['user', 'answer']
    answer = models.ForeignKey("questions.Answer", verbose_name = "Ответ", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
