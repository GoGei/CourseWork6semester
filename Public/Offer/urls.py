from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<offer_id>\d+)/$', views.offer_view, name='offer-view'),
]
