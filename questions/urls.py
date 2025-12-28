from django.urls import re_path
from questions.views import IndexView, DetailView, QuestionAskView, QuestionsTagView, \
    QuestionsHotView, LikeQuestionView, LikeAnswerView, CheckAnswerView

app_name = "questions"
urlpatterns = [
    re_path(r'^(?P<id>\d+)/like/', LikeQuestionView.as_view(), name="questionlike"),
    re_path(r'^answers/(?P<id>\d+)/check/', CheckAnswerView.as_view(), name="checkanswer"),
    re_path(r'^answers/(?P<id>\d+)/like/', LikeAnswerView.as_view(), name="answerlike"),
    re_path(r'^hot/', QuestionsHotView.as_view(), name="questions_hot"),
    re_path(r'^(?P<pk>\d+)/detail/', DetailView.as_view(), name="question_detail"),
    re_path(r'^tag/(?P<pk>\w+)/', QuestionsTagView.as_view(), name="questions_tag"),
    re_path(r'^ask/', QuestionAskView.as_view(), name="question_ask"),
    re_path(r'^', IndexView.as_view(), name="index_question_view"),
]