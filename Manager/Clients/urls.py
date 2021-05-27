from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.user_list, name='user-list'),
    url(r'^(?P<user_id>\d+)/details/$', views.user_details, name='user-details'),
]
