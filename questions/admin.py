from django.contrib import admin
from questions.models import Question, Answer, QuestionLike, AnswerLike, Tag
from core.models import Profile 

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "likes", "dislikes", "answers_cnt", "is_active"]
    filter_horizontal = ["tags"]
    raw_id_fields = ["author"]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["author", "likes", "dislikes", "is_active"]

@admin.register(AnswerLike)
class AnswerLikesAdmin(admin.ModelAdmin):
    ...

@admin.register(QuestionLike)
class QuestionLikesAdmin(admin.ModelAdmin):
    ...

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ...

