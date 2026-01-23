from django.db import models, IntegrityError
from django.db.models import Count
from django.core.cache import cache
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.search import SearchVector, TrigramSimilarity

def get_cached_popular_tags():
    tags = cache.get("TAGS")
    return tags

def get_cached_best_members(limit=5):
    best_members = cache.get("MEMBERS")
    return best_members

def search_by_query(query):
    from questions.models import Question
    if (len(query) < 3):
        return Question.objects.hot()[:5]
    questions = Question.objects.annotate(
        search=SearchVector('title', 'content'),
        similarity=TrigramSimilarity('title', query)
    ).filter(search=query).order_by('-similarity')[:5]
    return questions

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
                user_like.is_active = True
                user_like.save(update_fields=["type", "is_active"])
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
                user_like.is_active = True
                user_like.save(update_fields=["type", "is_active"])
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
                user_like.is_active = True
                user_like.save(update_fields=["type", "is_active"])
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
                user_like.is_active = True
                user_like.save(update_fields=["type", "is_active"])
                return 1 if user_like.type else -1
            else:
                user_like.is_active = not user_like.is_active
                user_like.save(update_fields=["is_active"])
                return (1 if user_like.type else -1) if user_like.is_active else 0
        return 1 if user_like.type else -1
    
def set_likes(object_list, user_likes_dict):
    for obj in object_list:
        if obj.id in user_likes_dict:
            if user_likes_dict[obj.id]: 
                obj.is_liked = 1
            else:
                obj.is_liked = -1
        else:
            obj.is_liked = 0

def set_user_question_likes(page_obj, request):
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
    
    set_likes(page_obj.object_list, user_likes_dict)
    return page_obj

def set_user_answer_likes(object_list, request):
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
    
    set_likes(object_list, user_likes_dict)
    return object_list

def set_user_question_like(question, request):
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
