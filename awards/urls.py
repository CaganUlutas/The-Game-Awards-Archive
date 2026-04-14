from django.urls import path
from . import views

app_name = 'awards'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('game/<slug:slug>/', views.game_detail, name='game_detail'),
    path('year/<int:year>/', views.year_detail, name='year_detail'),
    path('hall-of-fame/', views.hall_of_fame, name='hall_of_fame'),
    path('top-games/', views.top_games, name='top_games'),
]
