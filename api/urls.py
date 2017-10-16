

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<version>[0-9]+)/register/$', views.register_client),
    url(r'^(?P<version>[0-9]+)/log_in/$', views.log_in_client),
    url(r'^(?P<version>[0-9]+)/close_account/$', views.close_account),
]
