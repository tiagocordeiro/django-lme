import quandl
import datetime
from decouple import config
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from sqlalchemy import create_engine

from .models import TimeSerie, LondonMetalExchange


def index(request):
    lme = LondonMetalExchange.objects.all().order_by('-date')[:30]

    context = {
        'lme': lme,
    }
    return render(request, 'index.html', context)


def periodo(request, date_from, date_to):
    date_from = datetime.datetime.strptime(date_from, '%d-%m-%Y')
    date_to = datetime.datetime.strptime(date_to, '%d-%m-%Y')
    lme = LondonMetalExchange.objects.filter(date__range=(date_from, date_to))

    context = {
        'lme': lme,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'index.html', context)


@login_required
def update_database(request):
    # lme = LondonMetalExchange.objects.all()
    timeseries = TimeSerie.objects.all()
    lista = []
    colunas = []
    for serie in timeseries:
        lista.append(serie.code)
        colunas.append(serie.name)

    todo_periodo = quandl.get(lista,
                              start_date='2012-01-03',
                              returns='pandas')

    todo_periodo.columns = colunas

    engine = create_engine(config('DATABASE_URL'))

    connection = engine.connect()

    todo_periodo.to_sql('core_londonmetalexchange', connection, if_exists='replace', index=True)
    todo_periodo.to_csv('cotacao.csv')

    connection.close()

    context = {
        'timeseries': timeseries,
        'lista': lista,
        'todo_periodo': todo_periodo,
        'colunas': colunas,
        # 'lme': lme,
    }

    return render(request, 'update_database.html', context)
