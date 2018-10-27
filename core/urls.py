from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('periodo/<date_from>/<date_to>', views.periodo, name='periodo'),
    path('updatedb/', views.update_database, name='update_database'),
]
