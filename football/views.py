from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import nfldb

# Create your views here.
def index(request):
    """
    Home page of site
    """

    db = nfldb.connect()
    q = nfldb.Query(db)
    q.game(season_year=2015, season_type='Regular')
    
    paginator = Paginator(q.sort('passing_yds').as_aggregate(), 20)

    page = request.GET.get('page')
    try:
        stats = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, return the first page
        stats = paginator.page(1)
    except EmptyPage:
        # if page is out of range, return the past page
        stats = paginator.page(paginator.num_pages)

    return render(request, 'index.html', { 'stats': stats })
