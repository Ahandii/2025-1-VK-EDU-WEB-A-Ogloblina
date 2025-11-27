from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User

def get_best_members(limit=5):
    return User.objects.annotate(
        answers_count=Count('answer',
            filter=models.Q(answer__is_active=True, answer__is_correct=True)))\
            .filter(answers_count__gt=0)\
            .order_by('-answers_count')[:limit]

class QuestionManager(models.Manager):
    def active(self):
        return self.filter(is_active=1)\
            .select_related("author")\
            .prefetch_related("tags") \
            .order_by("-created_at")
    def hot(self):
        return self.filter(is_active=True) \
            .select_related("author") \
            .prefetch_related("tags") \
            .order_by("-answers_cnt", "-created_at")
    def tag(self, tag_id):
        return self.filter(tags__id=tag_id)\
            .select_related("author")\
            .prefetch_related("tags") \
            .order_by("-created_at")
 
class AnswerManager(models.Manager):
    def answers_by_question_id(self, id):
        from questions.models import Answer
        return Answer.objects.filter(question_id=id)\
            .order_by("created_at")\
            .only("is_correct", "content", "likes", "dislikes")

class TagManager(models.Manager):
    def with_questions_count(self):
        return self.annotate(questions_count=Count('question'))
    def popular_tags(self):
        return self.with_questions_count().order_by('-questions_count')[:10]