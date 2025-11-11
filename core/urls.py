from django.urls import re_path
from core.views import LoginView, SignupView, SettingsView

app_name = "core"
urlpatterns = [
    re_path(r'^login/', LoginView.as_view(), name="login"),
    re_path(r'^signup/', SignupView.as_view(), name="signup"),
    re_path(r'^settings/', SettingsView.as_view(), name="settings"),
]