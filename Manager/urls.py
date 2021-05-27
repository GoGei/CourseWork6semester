from django.conf.urls import include, url

from Manager.Login import views

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'', include('Manager.Home.urls')),
    url(r'^clients/', include('Manager.Clients.urls')),
    url(r'^managers/', include('Manager.Managers.urls')),
    url(r'^offers/', include('Manager.Offers.urls')),
    url(r'^offer-requests/', include('Manager.OfferRequests.urls')),
    url(r'^login/$', views.manager_login, name='manager-login'),
    url(r'^logout/$', views.manager_logout, name='manager-logout'),
]
