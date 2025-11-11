from django.contrib import admin
from questions.models import Profile, Question, Answer, QuestionLikes, AnswerLikes, Tag

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    ...

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    ...

@admin.register(AnswerLikes)
class AnswerLikesAdmin(admin.ModelAdmin):
    ...

@admin.register(QuestionLikes)
class QuestionLikesAdmin(admin.ModelAdmin):
    ...

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ...

