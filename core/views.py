import datetime
from datetime import datetime, timedelta

import pandas as pd
import quandl
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


def chart(request, chart_id='chart_ID', chart_type='line', chart_height=350):
    lme = LondonMetalExchange.objects.all().order_by('-date')

    lme_last = LondonMetalExchange.objects.values('date').last()

    date_to = lme_last['date']
    date_from = date_to - timedelta(weeks=5)

    lme_periodo = LondonMetalExchange.objects.filter(date__range=(date_from, date_to))

    df = pd.DataFrame(list(lme_periodo.values('date', 'cobre', 'zinco', 'aluminio',
                                              'chumbo', 'estanho', 'niquel', 'dolar', )))

    df['date'] = pd.to_datetime(df['date'], utc=True)

    df = df.set_index(df['date'])

    df = df.drop('date', axis=1)

    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    cobre = [float(item) for item in list(df['cobre'])]
    zinco = [float(item) for item in list(df['zinco'])]
    aluminio = [float(item) for item in list(df['aluminio'])]
    chumbo = [float(item) for item in list(df['chumbo'])]
    estanho = [float(item) for item in list(df['estanho'])]
    niquel = [float(item) for item in list(df['niquel'])]
    dolar = [float(item) for item in list(df['dolar'])]
    data = list(df.index.strftime('%d/%m/%y'))

    chart = {"renderTo": chart_id, "type": chart_type,
             "height": chart_height}

    series = [{"name": 'Cobre', "data": cobre},
              {"name": 'Zinco', "data": zinco},
              {"name": 'Alumínio', "data": aluminio},
              {"name": 'Chumbo', "data": chumbo},
              {"name": 'Estanho', "data": estanho},
              {"name": 'Níquel', "data": niquel},
              {"name": 'Dolar', "data": dolar}
              ]

    title = {"text": 'Cotação LME'}
    xAxis = {"categories": data, "crosshair": 'true'}
    yAxis = {"title": {"text": 'Valor'}}

    context = {
        'lme': lme,
        'xAxis': xAxis,
        'yAxis': yAxis,
        'series': series,
        'title': title,
        'chart': chart,
        'chart_id': chart_id,
        'lme_last': lme_last['date'],
        'date_to': date_to,
        'date_from': date_from,
        'lme_periodo': lme_periodo,
    }

    return render(request, 'chart.html', context)


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


def chart_periodo(request, date_from, date_to, chart_id='chart', chart_type='line', chart_height=350):
    date_from = datetime.strptime(date_from, '%d-%m-%Y')
    date_to = datetime.strptime(date_to, '%d-%m-%Y')
    lme = LondonMetalExchange.objects.filter(date__range=(date_from, date_to))

    df = pd.DataFrame(list(lme.values('date', 'cobre', 'zinco', 'aluminio',
                                      'chumbo', 'estanho', 'niquel', 'dolar', )))

    df['date'] = pd.to_datetime(df['date'], utc=True)

    df = df.set_index(df['date'])

    df = df.drop('date', axis=1)

    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    cobre = [float(item) for item in list(df['cobre'])]
    zinco = [float(item) for item in list(df['zinco'])]
    aluminio = [float(item) for item in list(df['aluminio'])]
    chumbo = [float(item) for item in list(df['chumbo'])]
    estanho = [float(item) for item in list(df['estanho'])]
    niquel = [float(item) for item in list(df['niquel'])]
    dolar = [float(item) for item in list(df['dolar'])]
    data = list(df.index.strftime('%d/%m/%y'))

    chart = {"renderTo": chart_id, "type": chart_type,
             "height": chart_height}

    series = [{"name": 'Cobre', "data": cobre},
              {"name": 'Zinco', "data": zinco},
              {"name": 'Alumínio', "data": aluminio},
              {"name": 'Chumbo', "data": chumbo},
              {"name": 'Estanho', "data": estanho},
              {"name": 'Níquel', "data": niquel},
              {"name": 'Dolar', "data": dolar}
              ]

    title = {"text": 'Cotação LME'}
    xAxis = {"categories": data, "crosshair": 'true'}
    yAxis = {"title": {"text": 'Valor'}}

    context = {
        'lme': lme,
        'xAxis': xAxis,
        'yAxis': yAxis,
        'series': series,
        'title': title,
        'chart': chart,
        'chart_id': chart_id,
    }

    return render(request, 'chart.html', context)


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
