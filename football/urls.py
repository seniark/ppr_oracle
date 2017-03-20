from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),

        url(r'^teams/$',  views.TeamListView.as_view(), name='teams'),
        url(r'^teams/(?P<pk>[A-Z]{2,3})/$', views.TeamDetailView.as_view(), name='team-detail'),

        url(r'^players/$', views.PlayerListView.as_view(), name='players'),

        url(r'^players/quarterbacks/$', views.players_quarterbacks, name='pos-qb'),
        url(r'^players/quarterbacks/(?P<year>[0-9]{4})/$', views.players_quarterbacks, name='pos-qb'),
        url(r'^players/quarterbacks/(?P<year>[0-9]{4})/(?P<phase>\w+)/$', views.players_quarterbacks, name='pos-qb'),
        url(r'^players/quarterbacks/(?P<year>[0-9]{4})/(?P<phase>\w+)/(?P<week>(\d+|All))/$', views.players_quarterbacks, name='pos-qb'),

        url(r'^players/runningbacks/$', views.players_runningbacks, name='pos-rb'),
        url(r'^players/runningbacks/(?P<year>[0-9]{4})/$', views.players_runningbacks, name='pos-rb'),
        url(r'^players/runningbacks/(?P<year>[0-9]{4})/(?P<phase>\w+)/$', views.players_runningbacks, name='pos-rb'),
        url(r'^players/runningbacks/(?P<year>[0-9]{4})/(?P<phase>\w+)/(?P<week>(\d+|All))/$', views.players_runningbacks, name='pos-rb'),

        url(r'^players/widereceivers/$', views.players_widereceivers, name='pos-wr'),
        url(r'^players/widereceivers/(?P<year>[0-9]{4})/$', views.players_widereceivers, name='pos-wr'),
        url(r'^players/widereceivers/(?P<year>[0-9]{4})/(?P<phase>\w+)/$', views.players_widereceivers, name='pos-wr'),
        url(r'^players/widereceivers/(?P<year>[0-9]{4})/(?P<phase>\w+)/(?P<week>(\d+|All))/$', views.players_widereceivers, name='pos-wr'),
]
