from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.core.paginator import Paginator

def index_view(request):
    questions = []
    for i in range(50):
        questions.append(
            {
                "id": i,
                "text": f"LONG_TEXT {i}",
                "description": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Esse possimus minima officiis iure? Commodi illo quibusdam voluptates accusantium id deleniti natus nobis explicabo tempore? Porro, assumenda. Rem cumque"
            }
        )
    page_number = request.GET.get("page", 1)
    page = Paginator(questions, per_page=5)

    items_list = page.page(page_number)

    return render(request, "index.html", context={"object_list": items_list, "page_obj": page})

class DetailView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
