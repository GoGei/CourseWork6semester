from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.manager_list, name='manager-list'),
    url(r'^add/$', views.manager_add, name='manager-add'),
    url(r'^(?P<manager_id>\d+)/edit/$', views.manager_edit, name='manager-edit'),
    url(r'^(?P<manager_id>\d+)/details/$', views.manager_details, name='manager-details'),
    url(r'^(?P<manager_id>\d+)/delete/$', views.manager_delete, name='manager-delete'),
]
