from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.sessions.models import Session
from .forms import SignUpForm
from .models import Category, Article


class IndexView(ListView):
    model = Article
    template_name = 'articles/index.html'


class MyLoginView(LoginView):
    template_name = 'articles/login.html'
    redirect_field_name = '/articles/success'

    def get_success_url(self, **kwargs):
        return reverse_lazy('success')


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'articles/sign_up.html'
    success_url = '/articles/success'

    def form_valid(self, form):
        valid = super().form_valid(form)
        user = authenticate(username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('password1'))
        login(self.request, user)
        return valid


class SuccessView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'articles/authorized.html'
    model = Article

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        session_id = self.request.COOKIES.get('sessionid')
        session = Session.objects.get(session_key=session_id)
        uid = session.get_decoded().get('_auth_user_id')
        context['name'] = User.objects.get(pk=uid)
        return context

