from django.db import models

class QuestionManager(models.Manager):
    def active(self):
        return self.filter(is_active=1).\
            select_related("author").\
            order_by("-created_at").\
            only("title", "author", "answer", "likes", "is_active", "created_at")
    def hot(self):
        print("snjhdsfh")
        queryset = self.filter(is_active=1).\
            select_related("author").\
            order_by("-answers_cnt").\
            order_by("-created_at").\
            only("title", "author", "answer", "likes", "is_active", "created_at")

        for q in queryset[:5]:
            print(f"Question {q.id}: answers_cnt={q.answers_cnt}")
        return queryset
    def tag(self, tag_name=""):
        if not tag_name:
            return self.none()
        else:
            from questions.models import Tag
            if Tag.objects.filter(name=tag_name).exists():
                return self.filter(tags__name=tag_name).\
                order_by("-created_at").\
                only("title", "author", "answer", "likes", "is_active", "created_at")
            else:
                return self.none()
            

     
    
