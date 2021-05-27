from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.account_user, name='account'),
    url(r'^add-to-viewed/(?P<offer_id>\d+)/$', views.account_add_to_viewed, name='account-add-to-viewed'),
    url(r'^remove-from-viewed/(?P<offer_request_id>\d+)/$', views.account_remove_from_viewed, name='account-remove-from-viewed'),
]
