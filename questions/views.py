from django.core.paginator import Paginator
from django.views.generic import TemplateView
from questions.models import Question, Answer, Tag, User
from django.http import Http404

def paginate(objects_list, request, per_page=10):
    page_number = request.GET.get("page", 1)
    paginator = Paginator(objects_list, per_page=per_page)
    page_obj = paginator.get_page(page_number)
    return page_obj

class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        popular_tags = Tag.objects.popular_tags()
        best_members = User.objects.all()[:5] #заглушка на время
        context["popular_tags"] = popular_tags
        context["best_members"] = best_members
        return context

class IndexView(BaseView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.active()
        page_obj = paginate(questions, self.request)
        context["page_obj"] = page_obj
        return context

class QuestionsHotView(BaseView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.hot()
        page_obj = paginate(questions, self.request)
        context["page_obj"] = page_obj
        return context

class DetailView(BaseView):
    template_name = "question.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("pk")
        try:
            context["question"] = Question.objects.get(pk=id)
            context["answers"] = Answer.objects.answers_by_question_id(id)
            return context
        except Question.DoesNotExist:
            raise Http404("Question does not exist")
        
class QuestionsTagView(BaseView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        tag_name = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        if not Tag.objects.filter(name=tag_name).exists():
            raise Http404("Tag doesn't exist")
        questions = Question.objects.tag(tag_name=tag_name)
        page_obj = paginate(questions, self.request)
        context["page_obj"] = page_obj
        context["tag"] = tag_name
        return context

class QuestionAskView(BaseView):
    template_name = "ask.html"
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
