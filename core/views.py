import quandl
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import TimeSerie


def index(request):
    return render(request, 'index.html')


@login_required
def update_database(request):
    timeseries = TimeSerie.objects.all()
    lista = []
    for serie in timeseries:
        lista.append(serie.code)

    todo_periodo = quandl.get(lista,
                              start_date='2012-01-03',
                              returns='pandas')

    context = {
        'timeseries': timeseries,
        'lista': lista,
        'todo_periodo': todo_periodo,
    }

    return render(request, 'update_database.html', context)
