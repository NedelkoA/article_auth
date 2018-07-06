from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Article


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
    telephone = forms.CharField(required=False)


class VerifyForm(forms.Form):
    code = forms.IntegerField(max_value=9999, min_value=1000)


class SettingsForm(forms.Form):
    two_factor = forms.BooleanField(required=False)
