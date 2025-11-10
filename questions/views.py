from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import TemplateView

def index_view(request):
    questions = []
    for i in range(50):
        questions.append(
            {
                "id": i,
                "text": f"LONG_TEXT {i}",
                "description": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Esse possimus minima officiis iure? Commodi illo quibusdam voluptates accusantium id deleniti natus nobis explicabo tempore? Porro, assumenda. Rem cumque",
                "answers": 3,
                "tags": ["black_jack", "bender"]
            }
        )
    page_number = request.GET.get("page", 1)
    paginator = Paginator(questions, per_page=5)

    page_obj = paginator.get_page(page_number)
    return render(request, "index.html", context={"object_list": page_obj.object_list, "page_obj": page_obj})

class DetailView(TemplateView):
    template_name = "question.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class QuestionAskView(TemplateView):
    template_name = "ask.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class QuestionsTagView(TemplateView):
    template_name = "questionstag.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
class QuestionsHotView(TemplateView):
    template_name = "questionshot.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
