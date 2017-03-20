from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
import nfldb

from .models import Team, Player

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

class TeamListView(generic.ListView):
    model = Team

class PlayerListView(generic.ListView):
    model = Player

class TeamDetailView(generic.DetailView):
    model = Team
