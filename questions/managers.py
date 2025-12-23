from django.db import models, IntegrityError
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
            .select_related("author__profile") \
            .prefetch_related("tags") \
            .order_by("-created_at")
    def hot(self):
        return self.filter(is_active=True) \
            .select_related("author") \
            .select_related("author__profile") \
            .prefetch_related("tags") \
            .order_by("-answers_cnt", "-created_at")
    def tag(self, tag_id):
        return self.filter(tags__id=tag_id)\
            .select_related("author")\
            .select_related("author__profile") \
            .prefetch_related("tags") \
            .order_by("-created_at")
 
class AnswerManager(models.Manager):
    def answers_by_question_id(self, id):
        from questions.models import Answer
        return Answer.objects.filter(question_id=id)\
            .order_by("created_at")\
            .select_related("author")\
            .select_related("author__profile") \

class TagManager(models.Manager):
    def with_questions_count(self):
        return self.annotate(questions_count=Count('question'))
    def popular_tags(self):
        return self.with_questions_count().order_by('-questions_count')[:10]
    
class QuestionLikeManager(models.Manager):
    def leave_like(self, question, user, type):
        from questions.models import QuestionLikes
        query = {"question": question, "user": user}
        user_like = self.filter(**query).first()
        if user_like is not None:
            if user_like.type != type:
                user_like.type = type
                user_like.save(update_fields=["type"])
                return 1 if user_like.type else -1
            else:
                user_like.is_active = not user_like.is_active
                user_like.save(update_fields=["is_active"])
                return (1 if user_like.type else -1) if user_like.is_active else 0
        try:
            user_like = QuestionLikes.objects.create(**query, type=type)
        except IntegrityError as db_error:
            print(db_error)
            user_like = self.filter(**query).first()
            if user_like.type != type:
                user_like.type = type
                user_like.save(update_fields=["type"])
                return 1 if user_like.type else -1
            else:
                user_like.is_active = not user_like.is_active
                user_like.save(update_fields=["is_active"])
                return (1 if user_like.type else -1) if user_like.is_active else 0
        return 1 if user_like.type else -1
    
class AnswerLikeManager(models.Manager):
    def leave_like(self, answer, user, type):
        from questions.models import AnswerLikes
        query = {"answer": answer, "user": user}
        user_like = self.filter(**query).first()
        if user_like is not None:
            if user_like.type != type:
                user_like.type = type
                user_like.save(update_fields=["type"])
                return 1 if user_like.type else -1
            else:
                user_like.is_active = not user_like.is_active
                user_like.save(update_fields=["is_active"])
                return (1 if user_like.type else -1) if user_like.is_active else 0
        try:
            user_like = AnswerLikes.objects.create(**query, type=type)
        except IntegrityError as db_error:
            print(db_error)
            user_like = self.filter(**query).first()
            if user_like.type != type:
                user_like.type = type
                user_like.save(update_fields=["type"])
                return 1 if user_like.type else -1
            else:
                user_like.is_active = not user_like.is_active
                user_like.save(update_fields=["is_active"])
                return (1 if user_like.type else -1) if user_like.is_active else 0
        return 1 if user_like.type else -1
    
def setLikes(object_list, user_likes_dict):
    for obj in object_list:
        if obj.id in user_likes_dict:
            if user_likes_dict[obj.id]: 
                obj.is_liked = 1
            else:
                obj.is_liked = -1
        else:
            obj.is_liked = 0

def setUserQuestionLikes(page_obj, request):
    if not request.user.is_authenticated:
        for obj in page_obj.object_list:
            obj.is_liked = 0
        return page_obj
    question_ids = [obj.id for obj in page_obj.object_list]
    from questions.models import QuestionLikes
    user_likes = QuestionLikes.objects.filter(
        user=request.user,
        question_id__in=question_ids,
        is_active=True  
    ).values_list('question_id', 'type')
    
    user_likes_dict = {question_id: type for question_id, type in user_likes}
    
    setLikes(page_obj.object_list, user_likes_dict)
    return page_obj

def setUserAnswerLikes(object_list, request):
    if not request.user.is_authenticated:
        for obj in object_list:
            obj.is_liked = 0
        return object_list
    answer_ids = [obj.id for obj in object_list]
    from questions.models import AnswerLikes
    user_likes = AnswerLikes.objects.filter(
        user=request.user,
        answer_id__in=answer_ids,
        is_active=True  
    ).values_list('answer_id', 'type')
    
    user_likes_dict = {answer_id: type for answer_id, type in user_likes}
    
    setLikes(object_list, user_likes_dict)
    return object_list

def setUserQuestionLike(question, request):
    from questions.models import QuestionLikes
    if not request.user.is_authenticated:
        question.is_liked = 0
        return question
    user_like = QuestionLikes.objects.filter(user=request.user, question=question, is_active=True).first()
    if user_like:
        if user_like.type == 1:
            question.is_liked = 1
        else:
            question.is_liked = -1
    else:
        question.is_liked = 0
    return question
