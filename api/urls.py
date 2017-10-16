

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<version>[0-9]+)/register/$', views.register_client),
    url(r'^(?P<version>[0-9]+)/log_in/$', views.log_in_client),
    url(r'^(?P<version>[0-9]+)/close_account/$', views.close_account),
    url(r'^(?P<version>[0-9]+)/profile/$', views.client_profile),
    url(r'^(?P<version>[0-9]+)/pending_accounts/$', views.manager_pending_accounts),
    url(r'^(?P<version>[0-9]+)/approve/(?P<client_id>[0-9]+)/active/$', views.manager_approve_active),
    url(r'^(?P<version>[0-9]+)/approve/(?P<client_id>[0-9]+)/delete/$', views.manager_approve_delete),
]
