from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from questions.views import BaseView
from core.forms import LoginForm, ProfileForm, SignupForm
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from core.models import Profile
from questionproject import settings
from django.contrib import messages

class LoginView(FormView, BaseView):
    http_method_names = ["get", "post"]
    template_name = "login.html"
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("core:settings"))
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = auth.authenticate(
            self.request, 
            username=form.cleaned_data['login'], 
            password=form.cleaned_data['password']
        )
        if user:
            auth.login(self.request, user)
            next = self.request.GET.get("next")
            messages.success(self.request, message="You successfull logged in!")
            return HttpResponseRedirect(reverse('core:settings'))
    
        form.add_error(None, "Incorrect login or password")
        return self.form_invalid(form)

# def login_view(request):

#     form = LoginForm()
#     if request.method == "POST":
#         form = LoginForm(data=request.POST)

#         if form.is_valid():
#             print(form.cleaned_data)
#             user = auth.authenticate(
#                 request, 
#                 username=form.cleaned_data['login'], 
#                 password=form.cleaned_data['password']
#             )
#             print(form.cleaned_data)
#             print(user)
#             if user:
#                 auth.login(request, user)
#                 return redirect(reverse("core:settings"))
        
#             form.add_error(None, "Incorrect login or password")
#     return render(request, "login.html", context={"form": form}) 
    
class SignupView(FormView, BaseView):
    template_name = "signup.html"  
    form_class = SignupForm
        
    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return HttpResponseRedirect(reverse('core:settings'))
    
    def success_url(self):
        return reverse("core:settings")


def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("core:login"))

class SettingsView(LoginRequiredMixin, FormView, BaseView):
    http_method_names = ['post', 'get']
    template_name = "settings.html"
    form_class = ProfileForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    def success_url(self):
        return reverse("core:settings")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.filter(user__id=self.request.user.pk).first()
        if profile and profile.avatar:
            context["avatar"] = profile.avatar.url
        else:
            context["avatar"] = settings.MEDIA_URL + "avatars/no-avatar.jpeg"
        return context 
  
