from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
import nfldb

from .models import Team, Player, PlayPlayer

# Create one instance of the db per process

# Create your views here.
def index(request):
    """
    Home page of site
    """

    return render(request, 'index.html')

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

def players_quarterbacks(request, year="2016", phase="All", week="All"):
    db = nfldb.connect()
    q = nfldb.Query(db)

    q.game(season_year=year)

    weeks = []
    if phase != 'All':
        q.game(season_type=phase)

        if phase == 'Preseason':
            weeks += ["All", "1", "2", "3", "4"]
        elif phase == 'Regular':
            weeks += ["All", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]
        elif phase == 'Postseason':
            weeks += ["All", "1", "2", "3", "4"]

        if week != 'All':
            q.game(week=week)

    q.player(position='QB')

    page = request.GET.get('page')
    stats = players_paginate(q.sort('passing_yds').as_aggregate(), page)

    return render(request, 'positions/quarterbacks.html',
            { 'position': 'Quarterbacks',
                'urlId': 'pos-qb',
                'year': year,
                'phase': phase,
                'weeks': weeks,
                'week': week,
                'stats': stats })

def players_runningbacks(request, year="2016", phase="All", week="All"):
    """
    Listing of running backs
    """

    db = nfldb.connect()
    q = nfldb.Query(db)

    q.game(season_year=year)

    weeks = []
    if phase != 'All':
        q.game(season_type=phase)

        if phase == 'Preseason':
            weeks += ["All", "1", "2", "3", "4"]
        elif phase == 'Regular':
            weeks += ["All", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]
        elif phase == 'Postseason':
            weeks += ["All", "1", "2", "3", "4"]

        if week != 'All':
            q.game(week=week)

    q.player(position='RB')

    page = request.GET.get('page')
    stats = players_paginate(q.sort('rushing_yds').as_aggregate(), page)

    return render(request, 'positions/runningbacks.html', 
            { 'position': 'Running Backs',
                'urlId': 'pos-rb',
                'year': year,
                'phase': phase,
                'weeks': weeks,
                'week': week,
                'stats': stats })

def players_widereceivers(request, year="2016", phase="All", week="All"):
    """
    Listing of wide receivers
    """
    db = nfldb.connect()
    q = nfldb.Query(db)

    # Get the list of filters
    q.game(season_year=year)

    weeks = []
    if phase != 'All':
        q.game(season_type=phase)

        if phase == 'Preseason':
            weeks += ["All", "1", "2", "3", "4"]
        elif phase == 'Regular':
            weeks += ["All", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]
        elif phase == 'Postseason':
            weeks += ["All", "1", "2", "3", "4"]

        if week != 'All':
            q.game(week=week)

    q.player(position='WR')

    page = request.GET.get('page')
    stats = players_paginate(q.sort('receiving_yds').as_aggregate(), page)

    return render(request, 'positions/widereceivers.html', 
            { 'position': 'Wide Receivers',
                'urlId': 'pos-wr',
                'year': year,
                'phase': phase,
                'weeks': weeks,
                'week': week,
                'stats': stats })

class TeamListView(generic.ListView):
    model = Team

class PlayerListView(generic.ListView):
    model = Player

class PlayPlayerListView(generic.ListView):
    model = PlayPlayer
