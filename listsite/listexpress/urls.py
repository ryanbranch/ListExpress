from django.conf.urls import url

from . import views

app_name = 'listexpress'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /list/5/
    url(r'^list/(?P<itemlist_id>[0-9]+)/$', views.listdetail, name='listdetail'),
]