from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.core.cache import caches
from .forms import SignUpForm, ArticleForm, CategoryForm, VerifyForm, SettingsForm
from .models import Category, Article, UserProfile
from .utils.telegram_bot import bot, handle
from random import randint
import logging


logger = logging.getLogger('manual')
cache = caches['my_cache']


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
        user = User.objects.get(username=form.cleaned_data.get('username'))
        profile = UserProfile.objects.get(user=user)
        if profile.telegram_id:
            user_id = user.id
            code = randint(1000, 9999)
            cache.set(user_id, code, 300)
            bot.sendMessage(profile.telegram_id, code)
            return redirect('verify', pk=user_id)
        logger.info(form.cleaned_data['username'] + ' is logged.')
        return super().form_valid(form)


class VerifyView(FormView):
    template_name = 'articles/verificate.html'
    form_class = VerifyForm
    success_url = '/articles/'

    def form_valid(self, form):
        check_code = cache.get(self.kwargs['pk'])
        current_user = User.objects.get(id=self.kwargs['pk'])
        cache.delete(self.kwargs['pk'])
        if check_code == form.cleaned_data.get('code'):
            login(self.request,
                  current_user,
                  backend='django.contrib.auth.backends.ModelBackend')
            logger.info(current_user.username + ' is logged.')
        else:
            return redirect('login')
        return super().form_valid(form)


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'articles/sign_up.html'
    success_url = '/articles/'

    def form_valid(self, form):
        valid = super().form_valid(form)
        user = authenticate(username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('password1'))
        login(self.request, user)
        logger.info(form.cleaned_data.get('username') + ' is signed up.')
        profile = UserProfile.objects.get(user=user)
        profile.telephone = form.cleaned_data.get('telephone')
        profile.save()
        return valid


class SettingsView(LoginRequiredMixin, FormView):
    form_class = SettingsForm
    login_url = 'login'
    success_url = 'settings'
    template_name = 'articles/settings.html'

    def form_valid(self, form):
        if form.cleaned_data.get('two_factor'):
            return render(self.request, self.template_name, {'link': True, 'form': form})
        else:
            session_key = self.request.session.session_key
            session = Session.objects.get(session_key=session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
            profile = UserProfile.objects.get(user=user)
            profile.telegram_id = None
            profile.save()
        return super().form_valid(form)


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

    def get(self, request, *args, **kwargs):
        try:
            Article.objects.get(id=kwargs['pk'])
        except Article.DoesNotExist:
            return redirect('index')
        return super().get(request, *args, **kwargs)


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


class AdminPanelView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'articles/admin_panel.html'
    login_url = 'login'
    redirect_field_name = '/articles/'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('index')
        return super().get(request, *args, **kwargs)


class ChangeStatusUserView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    fields = ['is_staff']
    permission_required = 'auth.change_group'
    login_url = 'login'
    template_name = 'articles/status_user.html'
    success_url = '/articles/'

    def form_valid(self, form):
        valid = super().form_valid(form)
        user = User.objects.get(pk=self.kwargs['pk'])
        user.groups.clear()
        if form.cleaned_data.get('is_staff'):
            group = Group.objects.get(name='Staff group')
        else:
            group = Group.objects.get(name='User group')
        group.user_set.add(user)
        return valid
