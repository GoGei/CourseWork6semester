
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.deal_list, name='deal-list'),
    url(r'^(?P<deal_id>\d+)/$', views.deal_details, name='deal-details'),
    url(r'^(?P<deal_id>\d+)/export/$', views.deal_export, name='deal-export'),
]
