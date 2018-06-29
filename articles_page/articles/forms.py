from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category, Article


class CategoryForm(forms.Form):
    class Meta:
        model = Category
        fields = '__all__'


class ArticleForm(forms.Form):
    class Meta:
        model = Article
        fields = '__all__'


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
