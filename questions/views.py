from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from questions.models import Question, Answer

from django.db.models import Count

def paginate(objects_list, request, per_page=5):
    page_number = request.GET.get("page", 1)
    paginator = Paginator(objects_list, per_page=per_page)
    page_obj = paginator.get_page(page_number)
    return page_obj

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.active()
        page_obj = paginate(questions, self.request)
        context["page_obj"] = page_obj
        context["object_list"] = page_obj.object_list
        return context

class QuestionsHotView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.hot()
        page_obj = paginate(questions, self.request)
        context["page_obj"] = page_obj
        context["object_list"] = page_obj.object_list
        return context

class DetailView(TemplateView):
    template_name = "question.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO сделать проверку!!!
        id = self.kwargs.get("pk")
        # print(id)
        # print(id)

        try:
            context["question"] = Question.objects.get(pk=id)
            print("kjhflgkhdfgh", Question.objects.get(pk=id).id)
            context["answers"] = Answer.objects.filter(question_id=id).only("is_correct", "content")
            return context
            
        except self.model.DoesNotExist:
            print("Error")

# TODO проверить исключение
        
class QuestionsTagView(TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        tag_name = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)

        questions = Question.objects.tag(tag_name=tag_name)
        page_obj = paginate(questions, self.request)
        context["page_obj"] = page_obj
        context["object_list"] = page_obj.object_list
        context["tag"] = tag_name
        return context

class QuestionAskView(TemplateView):
    template_name = "ask.html"
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
