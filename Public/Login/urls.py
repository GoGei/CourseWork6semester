from django.conf.urls import url
from django.contrib.auth import views as auth_views

from Public.Login import views

urlpatterns = [
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
]
