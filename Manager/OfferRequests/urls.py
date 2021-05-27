from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.offer_request_list, name='offer-request-list'),
    url(r'^(?P<offer_request_id>\d+)/details/$', views.offer_request_details, name='offer-request-details'),
    url(r'^(?P<offer_request_id>\d+)/approve/$', views.offer_request_approve, name='offer-request-approve'),
    url(r'^(?P<offer_request_id>\d+)/decline/$', views.offer_request_decline, name='offer-request-decline'),
    url(r'^(?P<offer_request_id>\d+)/restore/$', views.offer_request_restore, name='offer-request-restore'),
    url(r'^counter/$', views.offer_request_counter, name='offer-request-counter'),
]
