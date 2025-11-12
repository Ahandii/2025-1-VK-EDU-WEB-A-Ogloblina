from django.db import models
    
class QuestionManager(models.Manager):
    def active(self):
        return self.filter(is_active=1).\
            select_related("author").\
            order_by("-created_at").\
            only("title", "author", "answer", "likes", "is_active", "created_at")
    def hot(self):
        return self.filter(is_active=1).\
            select_related("author").\
            order_by("-answers_cnt", "-created_at").\
            only("title", "author", "answer", "likes", "is_active", "created_at")
    
    def tag(self, tag_name=""):
        return self.filter(tags__name=tag_name).\
            select_related("author").\
            order_by("-created_at").\
            only("title", "author", "answer", "likes", "is_active", "created_at")
 
class AnswerManager(models.Manager):
    def answers_by_question_id(self, id):
        from questions.models import Answer
        return Answer.objects.filter(question_id=id).\
            order_by("created_at").\
            only("is_correct", "content", "likes")

class TagManager(models.Manager):
    def popular_tags(self):
        return self.all()[:7]
    # TODO спросить (как эффективно считать и запоминать где-то популярные теги)
        # return self.objects.\
        #     annotate(tag_cnt = ).\
        #     order_by("-tag_cnt").all()[:7]
