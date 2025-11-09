from django.urls import re_path
from questions.views import DetailView, index_view

app_name = "questions"
urlpatterns = [
    re_path(r'^', index_view, name="index_question_view"),
    re_path(r'^(?P<pk>\d+)/detail/', DetailView.as_view(), name="question_detail"),
    re_path(r'^tag/', index_view, name="ask_question"),
    re_path(r'^hot/', index_view, name="hot_questions"),
    re_path(r'^login/', index_view, name="login"),
    re_path(r'^signup/', index_view, name="signup"),
    re_path(r'^ask/', index_view, name="ask_question"),
    
]