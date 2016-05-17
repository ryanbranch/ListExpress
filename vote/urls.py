from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.itemlist_list, name='itemlist_list'),
    url(r'^itemlist/(?P<pk>\d+)/$', views.itemlist_detail, name='itemlist_detail'),
    url(r'^itemlist/new/$', views.itemlist_new, name='itemlist_new'),
    url(r'^itemlist/(?P<pk>\d+)/edit/$', views.itemlist_edit, name='itemlist_edit'),
]