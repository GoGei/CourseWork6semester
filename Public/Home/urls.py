from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home_index, name='home-index'),
    url(r'^contacts/$', views.home_contacts, name='home-contacts'),
    url(r'^offers/$', views.home_offers, name='home-offers'),
    url(r'^about/$', views.home_about, name='home-about'),
]
