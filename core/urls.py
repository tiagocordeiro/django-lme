from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('updatedb/', views.update_database, name='update_database'),
]
