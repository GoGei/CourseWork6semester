from django.conf.urls import include, url

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'', include('Public.Home.urls')),
    url(r'', include('Public.Login.urls')),
    url(r'offer/', include('Public.Offer.urls')),
    url(r'register/', include('Public.Registration.urls')),
    url(r'account/', include('Public.Account.urls')),
]
