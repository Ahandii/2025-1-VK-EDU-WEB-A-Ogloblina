from django.urls import re_path
from questions.views import IndexView, DetailView, QuestionAskView, QuestionsTagView, QuestionsHotView

app_name = "questions"
urlpatterns = [
    re_path(r'^hot/', QuestionsHotView.as_view(), name="questions_hot"),
    re_path(r'^(?P<pk>\d+)/detail/', DetailView.as_view(), name="question_detail"),
    re_path(r'^tag/(?P<pk>\w+)/', QuestionsTagView.as_view(), name="questions_tag"),
    re_path(r'^ask/', QuestionAskView.as_view(), name="question_ask"),
    re_path(r'^', IndexView.as_view(), name="index_question_view"),
]