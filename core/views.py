from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = "login.html"
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
class SignupView(TemplateView):
    template_name = "signup.html"
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
class SettingsView(TemplateView):
    template_name = "settings.html"
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)