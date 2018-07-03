from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Article, CustomUser


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text', 'category', 'status']
        widgets = {
            'status': forms.HiddenInput(),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required. Inform a valid email address.')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'telephone', 'password1', 'password2']
