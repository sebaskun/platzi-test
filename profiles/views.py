from django.shortcuts import render

from django.urls import reverse_lazy

from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignupForm

class SignupUserView(FormView):
    form_class = SignupForm
    template_name = "profiles/signup.html"
    success_url = reverse_lazy("profiles:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class LoginUserView(LoginView):
    template_name = "profiles/login.html"

class LogoutUserView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy("profiles:login")


