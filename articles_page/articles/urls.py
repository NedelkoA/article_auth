from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'articles/$', views.IndexView.as_view(), name='index'),
    url(r'articles/login$', views.MyLoginView.as_view(), name='login'),
    url(r'articles/sign_up$', views.SignUpView.as_view(), name='sign_up'),
    url(r'articles/success$', views.SuccessView.as_view(), name='success'),
    url(r'articles/logout$', views.LogoutView.as_view(next_page='index'), name='logout')
]