from django.views.generic import TemplateView
from questions.views import BaseView

class LoginView(BaseView):
    template_name = "login.html"

    
class SignupView(BaseView):
    template_name = "signup.html"

    
class SettingsView(BaseView):
    template_name = "settings.html"
