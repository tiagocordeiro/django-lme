import quandl
from decouple import config
from django.core.management import BaseCommand
from sqlalchemy import create_engine

from core.models import TimeSerie


class Command(BaseCommand):
    help = '''Atualiza cotações no banco de dados'''

    def handle(self, *args, **options):
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

        todo_periodo.to_sql('core_londonmetalexchange', connection,
                            if_exists='replace', index=True)

        connection.close()
