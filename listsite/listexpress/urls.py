from django.conf.urls import url

from . import views

app_name = 'listexpress'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /list/5/
    url(r'^list/(?P<itemlist_id>[0-9]+)/$', views.listdetail, name='listdetail'),
    # ex: /list/5/buildcomparisons
    url(r'^list/(?P<itemlist_id>[0-9]+)/buildcomparisons/$', views.buildcomparisons, name='buildcomparisons'),
    # ex: /list/5/comparisonvote
    url(r'^list/(?P<itemlist_id>[0-9]+)/comparisonvote/$', views.comparisonvote, name='comparisonvote'),
    # ex: /list/5/comparisonvote with votedComparison_id and vote specified
    url(r'^list/(?P<itemlist_id>[0-9]+)/comparisonvote/(?P<votedComparison_id>[0-9]+)/(?P<vote>[0-9]?)/$', views.comparisonvote, name='comparisonvote'),
    #url(r'^blog/$', views.page),
    #url(r'^blog/page(?P<num>[0-9]+)/$', views.page),
]