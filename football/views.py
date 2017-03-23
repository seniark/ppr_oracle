from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.contrib.auth.models import User
import nfldb

from .models import Team, Player, UserTeam, UserPlayer
from .forms import CreateTeamForm

# Create one instance of the db per process

# Create your views here.
def index(request):
    """ Home page of site """
    return render(request, 'index.html', { 'page': 'home' })

def page_not_found(request):
    """ 404 Error Page """
    return render(request, 'page_not_found.html')

def build_query(year, phase, week):
    db = nfldb.connect()
    query = nfldb.Query(db)

    query.game(season_year=year)

    weeks = []
    if phase != 'All':
        if phase == 'Preseason':
            weeks += ["All", "1", "2", "3", "4"]
        elif phase == 'Regular':
            weeks += ["All", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]
        elif phase == 'Postseason':
            weeks += ["All", "1", "2", "3"]
        else:
            raise Http404("Page not found!")

        query.game(season_type=phase)

        if week != 'All':
            query.game(week=week)

    return (query, weeks)

def players_paginate(query, page):
    paginator = Paginator(query, 20)

    try:
        stats = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, return the first page
        stats = paginator.page(1)
    except EmptyPage:
        # if page is out of range, return the last page
        stats = paginator.page(paginator.num_pages)

    return stats

def team_create(request):
   
    if request.method == 'POST':
        form = CreateTeamForm(request.POST)

        # check if the form is valid
        if form.is_valid():
            ut = UserTeam()
            ut.team_name = form.cleaned_data['team_name']
            ut.user = User.objects.get(id=request.POST['user_id'])
            ut.save()

        return HttpResponseRedirect('/')
    else:
        # If this is a GET (or any other) request, create the form
        form = CreateTeamForm()

    return render(request, 'football/team_create.html', {'form': form })

def team_detail(request, pk):

    # Get the team object
    team = get_object_or_404(UserTeam, pk=pk)

    return render(request, 'football/team_detail.html', { 'team': team })


def add_player_to_team(request, player_id):

    if request.method == 'POST':
        # add players to selected teams
        for data in request.POST:
            if data != 'csrfmiddlewaretoken':
                up = UserPlayer()
                up.fantasy_team = UserTeam.objects.get(id=data)
                up.player = Player.objects.get(player_id=player_id)
                up.save()

    return HttpResponseRedirect('/')

def players_quarterbacks(request, year="2016", phase="All", week="All"):
    """ Listing of quarterbacks """
    (q, weeks) = build_query(year, phase, week)

    # Apply additional filters
    q.player(position='QB')

    page = request.GET.get('page')
    sort = request.GET.get('sort', 'passing_yds')

    stats = players_paginate(q.sort(sort).as_aggregate(), page)

    return render(request, 'positions/quarterbacks.html',
            { 'position': 'Quarterbacks',
                'urlId': 'pos-qb',
                'page': 'positions',
                'year': year,
                'phase': phase,
                'weeks': weeks,
                'week': week,
                'stats': stats })

def players_runningbacks(request, year="2016", phase="All", week="All"):
    """ Listing of running backs """
    (q, weeks) = build_query(year, phase, week)

    # Apply additional filters
    q.player(position='RB')

    page = request.GET.get('page')
    sort = request.GET.get('sort', 'rushing_yds')

    stats = players_paginate(q.sort(sort).as_aggregate(), page)

    return render(request, 'positions/runningbacks.html', 
            { 'position': 'Running Backs',
                'urlId': 'pos-rb',
                'page': 'positions',
                'year': year,
                'phase': phase,
                'weeks': weeks,
                'week': week,
                'stats': stats })

def players_widereceivers(request, year="2016", phase="All", week="All"):
    """ Listing of wide receivers """
    (q, weeks) = build_query(year, phase, week)

    # Apply additional filters
    q.player(position='WR')

    page = request.GET.get('page')
    sort = request.GET.get('sort', 'receiving_yds')

    stats = players_paginate(q.sort(sort).as_aggregate(), page)

    return render(request, 'positions/widereceivers.html', 
            { 'position': 'Wide Receivers',
                'urlId': 'pos-wr',
                'page': 'positions',
                'year': year,
                'phase': phase,
                'weeks': weeks,
                'week': week,
                'stats': stats })

class NflListView(generic.ListView):
    model = Team
    template_name = 'football/nfl_team_list.html'

class NflDetailView(generic.DetailView):
    model = Team
    template_name = 'football/nfl_team_detail.html'

class PlayerListView(generic.ListView):
    model = Player

