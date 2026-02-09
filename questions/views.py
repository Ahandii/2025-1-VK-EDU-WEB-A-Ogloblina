from django.views.generic import TemplateView, FormView
from questions.models import Question, Answer, Tag, QuestionLike, AnswerLike
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from questions.managers import get_cached_best_members, get_cached_popular_tags, \
    set_user_question_likes, set_user_answer_likes, set_user_question_like, search_by_query
from django.shortcuts import get_object_or_404, redirect
from questions.forms import QuestionForm, AnswerForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Profile 
from questionproject.settings import MEDIA_URL, CENTRIFUGO_HMAC_SECRET, CENTRIFUGO_URL, CENTRIFUGO_API_KEY
from rest_framework.views import APIView
from django.db import IntegrityError
from django.http import HttpResponseForbidden
import jwt
import time 
from cent import Client, PublishRequest
from utils.string import str_to_int
import json 
from rest_framework.permissions import IsAuthenticated 
from django.db.models import Sum, Case, When, IntegerField

def paginate(objects_list, request, per_page=10):
    page_number = request.GET.get("page", 1)
    paginator = Paginator(objects_list, per_page=per_page)
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger or EmptyPage:
        page_obj = paginator.get_page(1)
    return page_obj
    
def search_view(request):
    query = request.GET.get('q')
    if query and query.strip(): 
        questions = search_by_query(query.strip()) 
        quests = []
        for q in questions:
            quests.append({
                "id": q.id, 
                "title": q.title, 
                "content": q.content
            })
        return JsonResponse({"status": "ok", "questions": quests}, status=200)
    
    return JsonResponse({
        "status": "ok", 
        "questions": [],
        "message": "Введите поисковый запрос"
    }, status=200)

def generate_token(user_id):
    token = jwt.encode({
        "sub": str(user_id),
        "exp": int(time.time() * 10 * 60)
    }, CENTRIFUGO_HMAC_SECRET, algorithm = "HS256")
    return token

class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        popular_tags = get_cached_popular_tags()
        best_members = get_cached_best_members(5) 

        profile = Profile.objects.filter(user__id=self.request.user.pk).first()
        if profile:
            context["avatar"] = profile.get_avatar()
        context["popular_tags"] = popular_tags
        context["best_members"] = best_members
        return context

class IndexView(BaseView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.active()
        page_obj = paginate(questions, self.request)
        page_obj = set_user_question_likes(page_obj, self.request)
        context["page_obj"] = page_obj
        return context

class QuestionsHotView(BaseView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.hot()
        page_obj = paginate(questions, self.request)
        context["page_obj"] = page_obj
        context["hot"] = True
        return context

def publish_to_centrifugo(channel, data):
    api_url = f"http://{CENTRIFUGO_URL}/api"
    client = Client(api_url, CENTRIFUGO_API_KEY)
    request = PublishRequest(channel=channel, data=data)
    client.publish(request)

class QuestionDetailView(FormView, BaseView):
    form_class = AnswerForm
    template_name = "question.html"
    def dispatch(self, request, *args, **kwargs):
        id = self.kwargs.get("pk")
        question = Question.objects.filter(pk=id).first()
        if question is None:
            raise Http404("Question doesn't exist")
        self.question = set_user_question_like(question, self.request)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = self.question
        context["answers"] = set_user_answer_likes(Answer.objects.answers_by_question_id(self.question.pk), self.request)
        if self.request.user.is_authenticated:
            token = generate_token(self.request.user.pk)
        else:
            token = "UNAUTH"
        
        context["centrifugo_token"] = token
        context["centrifugo_url"] = CENTRIFUGO_URL
        context["centrifugo_channel"] = f"channel_{self.question.id}" 
        return context
    
    def form_valid(self, form):
        user = self.request.user
        if user.is_authenticated:
            form.instance.author = self.request.user
            form.instance.question = self.question
            answer = form.save()
            self.question.answers_cnt += 1
            self.question.save()
            profile = getattr(self.request.user, "profile", None)
            serialized_answer = {
                "id": answer.id,
                "content": answer.content,
                "author": {
                    "avatar": profile.get_avatar() if profile else "/static/avatars/no-avatar.jpeg" 
                },
                "is_liked": 0,
                "likes": 0, 
                "is_correct": False, 
                "question_author_id": self.question.author.id
            }
            publish_to_centrifugo(f"channel_{self.question.id}", {"message": serialized_answer})
            return HttpResponseRedirect(reverse('questions:question_detail', kwargs={'pk': self.question.pk}))
        return HttpResponseRedirect(reverse('core:login'))

class QuestionsTagView(BaseView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        tag_name = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        tag = Tag.objects.filter(name=tag_name).first()
        if tag is None:
            raise Http404("Tag doesn't exist")
        questions = Question.objects.tag(tag.pk)
        page_obj = paginate(questions, self.request)
        page_obj = set_user_question_likes(page_obj, self.request)
        context["page_obj"] = page_obj
        context["tag"] = tag_name
        return context

class QuestionAskView(LoginRequiredMixin, FormView, BaseView):
    http_method_names = ['get', 'post']
    template_name = "ask.html"
    form_class = QuestionForm
    
    def form_valid(self, form):
        user = self.request.user
        if user:
            form.instance.author = self.request.user
            question = form.save()
            return HttpResponseRedirect(reverse('questions:question_detail', kwargs={'pk': question.id}))
        else:
            return HttpResponseRedirect(reverse('core:login'))
        
class LikeQuestionView(APIView):
    http_method_names = [ 'post' ]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        question_id = kwargs["id"]
        question = Question.objects.filter(id=question_id).first()

        if question is None:
            return JsonResponse({"error": f"Question with id={question_id} not found"}, status=404)
        
        like_type = str_to_int(request.data.get("type"), 1)
        
        if like_type is None or like_type not in [0, 1]:
            return JsonResponse({"error": "Action request.data.get('type') not allowed"}, status=400)
        
        like_type = QuestionLike.objects.leave_like(user=request.user, question=question, type=like_type)

        question.likes = QuestionLike.objects.filter(question=question, is_active=True).aggregate(
            likes_diff=Sum(
                Case(
                    When(type=1, then=1),
                    When(type=0, then=-1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )['likes_diff'] or 0

        question.save(update_fields=["likes"])
        return JsonResponse({"status": "ok", "new_likes_count": question.likes, "type": like_type}, status = 200)
    
class LikeAnswerView(APIView):
    http_method_names = [ 'post' ]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        answer_id = kwargs["id"]  
        like_type = str_to_int(request.data.get("type"), 1)
        answer = Answer.objects.filter(id=answer_id).first()
        if answer is None:
            return JsonResponse({"error": f"Answer with id={answer_id} not found"}, status=404)
        
        if like_type is None or like_type not in [0, 1]:
            return JsonResponse({"error": "Action request.data.get('type') not allowed"}, status=400)
        
        like_type = AnswerLike.objects.leave_like(user=request.user, answer=answer, type=like_type)

        answer.likes = AnswerLike.objects.filter(answer=answer, is_active=True).aggregate(
            likes_diff=Sum(
                Case(
                    When(type=1, then=1),
                    When(type=0, then=-1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )['likes_diff'] or 0

        answer.save(update_fields=["likes"])
        return JsonResponse({"status": "ok", "new_likes_count": answer.likes, "type": like_type }, status = 200)
    
class CheckAnswerView(APIView):
    http_method_names = [ 'post' ]

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise HttpResponseForbidden("User is not authorized")
        answer_id = kwargs["id"]
        answer = Answer.objects.filter(id=answer_id).first()
        if answer is None:
            raise Http404("Answer doesn't exist")
        if answer.question.author == request.user:
            answer.is_correct = not answer.is_correct
            answer.save(update_fields=["is_correct"])
            return JsonResponse({"status": "ok", "is_correct": answer.is_correct }, status = 200)
        return HttpResponseForbidden("User is not an author")
