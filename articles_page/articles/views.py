from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .forms import SignUpForm, ArticleForm
from .models import Category, Article


class IndexView(ListView):
    model = Article
    template_name = 'articles/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class MyLoginView(LoginView):
    template_name = 'articles/login.html'
    redirect_field_name = '/articles/'

    def get_success_url(self, **kwargs):
        return reverse_lazy('index')


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'articles/sign_up.html'
    success_url = '/articles/'

    def form_valid(self, form):
        valid = super().form_valid(form)
        group = Group.objects.get(name='User group')
        user_current = User.objects.last()
        group.user_set.add(user_current)
        user = authenticate(username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('password1'))
        login(self.request, user)
        return valid


class CreateArticleView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = ArticleForm
    permission_required = 'articles.add_article'
    login_url = 'login'
    success_url = '/articles/'
    template_name = 'articles/new_article.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/detail_article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ArticleForm(instance=Article.objects.get(id=self.kwargs['pk']))
        return context


class ChangeArticleView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    fields = '__all__'
    permission_required = 'articles.change_article'
    login_url = 'login'
    success_url = '/articles/'
    template_name = 'articles/detail_article.html'


class ReviewArticlesView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles/review_articles.html'
    login_url = 'login'
    redirect_field_name = '/articles/review_articles'

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('index')
        return super().get(request, *args, **kwargs)


class ArticlesCategoryView(DetailView):
    model = Category
    template_name = 'articles/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(id=self.kwargs['pk'])
        return context
