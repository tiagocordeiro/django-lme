from datetime import datetime, timedelta

from .models import LondonMetalExchange


def get_last():
    last = LondonMetalExchange.objects.values('date').last()
    return str(datetime.strftime(last['date'] + timedelta(days=1), '%d-%m-%Y'))


def get_last_thirty_days():
    last = get_last()
    first = datetime.strptime(last, '%d-%m-%Y') - timedelta(days=30)
    return str(datetime.strftime(first, '%d-%m-%Y'))


def get_last_five_weeks():
    last = get_last()
    first = datetime.strptime(last, '%d-%m-%Y') - timedelta(weeks=5)
    return str(datetime.strftime(first, '%d-%m-%Y'))


def get_lme(date_from=get_last_five_weeks(), date_to=get_last(), limit=40):
    date_from = datetime.strptime(date_from, '%d-%m-%Y')
    date_to = datetime.strptime(date_to, '%d-%m-%Y')
    lme = LondonMetalExchange.objects.filter(date__range=(date_from, date_to))[:limit]
    return lme


def json_builder(lme_prices):
    itens_list = []
    for item in lme_prices:
        itens_list.append(
            {
                "data": item.date,
                "cobre": item.cobre,
                "zinco": item.zinco,
                "aluminio": item.aluminio,
                "chumbo": item.chumbo,
                "estanho": item.estanho,
                "niquel": item.niquel,
                "dolar": item.dolar
            }
        )
    return itens_list
