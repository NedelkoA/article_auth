from django.contrib import admin
from .models import Category, Article, UserProfile

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(UserProfile)
