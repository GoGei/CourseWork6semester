
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<state>\w+)/$', views.offer_list, name='offer-list'),

    url(r'^(?P<state>\w+)/(?P<offer_id>\d+)/add/file/$', views.offer_add_file, name='offer-add-file'),
    url(r'^(?P<state>\w+)/file/(?P<file_id>\d+)/delete/$', views.offer_delete_file, name='offer-delete-file'),

    url(r'^(?P<state>\w+)/add/$', views.offer_add, name='offer-add'),
    url(r'^(?P<state>\w+)/(?P<offer_id>\d+)/edit/$', views.offer_edit, name='offer-edit'),
    url(r'^(?P<state>\w+)/(?P<offer_id>\d+)/archive/$', views.offer_archive, name='offer-archive'),
    url(r'^(?P<state>\w+)/(?P<offer_id>\d+)/restore/$', views.offer_restore, name='offer-restore'),

    url(r'^(?P<state>\w+)/(?P<offer_id>\d+)/pick-up/$', views.offer_pick_up, name='offer-pick-up'),
    url(r'^(?P<state>\w+)/(?P<offer_id>\d+)/close/$', views.offer_close, name='offer-close'),
    url(r'^(?P<state>\w+)/(?P<offer_id>\d+)/deny/$', views.offer_deny, name='offer-deny'),
    url(r'^(?P<state>\w+)/(?P<offer_id>\d+)/recreate/$', views.offer_deny, name='offer-recreate'),

    url(r'^(?P<state>\w+)/(?P<offer_id>\d+)/$', views.offer_details, name='offer-details'),

    url(r'^(?P<state>\w+)/export/(?P<export_to>\w+)$', views.offer_export, name='offer-export'),
]
