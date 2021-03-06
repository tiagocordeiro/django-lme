from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.api_view, name='api'),
    path('api/<date_from>/<date_to>', views.api_view, name='api_periodo'),
    path('chart/', views.chart, name='chart'),
    path('grafico/', views.chart, name='grafico'),
    path('chart/<date_from>/<date_to>', views.chart, name='chart_periodo'),
    path('periodo/<date_from>/<date_to>', views.periodo, name='periodo'),
    path('cotacao/', views.group_by_week, name='group_by_week'),
    path('updatedb/', views.update_database, name='update_database'),
]
