from django.urls import path
from . import views
 
app_name = 'awards'
 
urlpatterns = [
    path('', views.home, name='home'),
    path('game/<slug:slug>/', views.game_detail, name='game_detail'),
    path('year/<int:year>/', views.year_detail, name='year_detail'),
]