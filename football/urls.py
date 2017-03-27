from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),

        url(r'^nfl/$',  views.NflListView.as_view(), name='nfl-teams'),
        url(r'^nfl/(?P<pk>[A-Z]{2,3})/$', views.NflDetailView.as_view(), name='nfl-team-detail'),

        url(r'^teams/create/$', views.team_create, name='team-create'),
        url(r'^teams/(?P<pk>\d+)/$', views.team_detail, name='team-detail'),

        url(r'^players/$', views.PlayerListView.as_view(), name='players'),
        url(r'^players/(?P<player_id>\d{2}-\d{7})/addtoteam/$', views.add_player_to_team, name='add-to-team'),
        url(r'^players/computepoints/$', views.players_compute_points, name='compute-points'),

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

        url(r'^players/tightends/$', views.players_tightends, name='pos-te'),
        url(r'^players/tightends/(?P<year>[0-9]{4})/$', views.players_tightends, name='pos-te'),
        url(r'^players/tightends/(?P<year>[0-9]{4})/(?P<phase>\w+)/$', views.players_tightends, name='pos-te'),
        url(r'^players/tightends/(?P<year>[0-9]{4})/(?P<phase>\w+)/(?P<week>(\d+|All))/$', views.players_tightends, name='pos-te'),
]
