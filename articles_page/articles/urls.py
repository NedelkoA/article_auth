from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'articles/$', views.IndexView.as_view(), name='index'),
    url(r'articles/login$', views.MyLoginView.as_view(), name='login'),
    url(r'articles/sign_up$', views.SignUpView.as_view(), name='sign_up'),
    url(r'articles/logout$', views.LogoutView.as_view(next_page='index'), name='logout'),
    url(r'articles/new_article$', views.CreateArticleView.as_view(), name='new_article'),
    url(r'articles/(?P<pk>[0-9]+)$', views.ArticleDetailView.as_view(), name='detail_article'),
    url(r'articles/review_articles$', views.ReviewArticlesView.as_view(), name='review_articles'),
    url(r'articles/(?P<pk>[0-9]+)/update$', views.ChangeArticleView.as_view(), name='update_article'),
    url(r'articles/category/(?P<pk>[0-9]+)$', views.ArticlesCategoryView.as_view(), name='articles_category'),
    url(r'articles/category/add$', views.CreateCategoryView.as_view(), name='add_category'),
]
