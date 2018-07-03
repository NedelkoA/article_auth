from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, ArticleForm, CategoryForm
from .models import Category, Article
import logging

logger = logging.getLogger('manual')


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
    success_url = '/articles/'

    def form_valid(self, form):
        logger.info(form.cleaned_data['username'] + ' is logged.')
        return super().form_valid(form)


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'articles/sign_up.html'
    success_url = '/articles/'

    def form_valid(self, form):
        valid = super().form_valid(form)
        user_current = User.objects.last()
        user = authenticate(username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('password1'))
        login(self.request, user)
        logger.info(user_current.username + ' is signed up.')
        return valid


class CreateArticleView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = ArticleForm
    permission_required = 'articles.add_article'
    login_url = 'login'
    success_url = '/articles/'
    template_name = 'articles/new_article.html'

    def form_valid(self, form):
        session_key = self.request.session.session_key
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        form.instance.user = user
        logger.info(user.username + ' created article ' + form.cleaned_data['title'] + ' in REVIEW status.')
        return super().form_valid(form)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/detail_article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ArticleForm(instance=Article.objects.get(id=self.kwargs['pk']))
        return context


class ChangeArticleView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    fields = ['title', 'text', 'status', 'category']
    permission_required = 'articles.change_article'
    login_url = 'login'
    success_url = '/articles/'
    template_name = 'articles/detail_article.html'

    def form_valid(self, form):
        logger.info('Staff user edited article ' +
                    form.cleaned_data['title'] + ' and set status LIVE.')
        return super().form_valid(form)


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


class CreateCategoryView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = CategoryForm
    permission_required = 'articles.add_category'
    login_url = 'login'
    success_url = '/articles/'
    template_name = 'articles/new_category.html'
