

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<version>[0-9]+)/register/$', views.register_client),
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
]
