from django.views.generic import TemplateView
from questions.views import BaseView

class LoginView(BaseView):
    template_name = "login.html"
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
class SignupView(BaseView):
    template_name = "signup.html"
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
class SettingsView(BaseView):
    template_name = "settings.html"
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)