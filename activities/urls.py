from django.urls import path
from . import views

urlpatterns = [
    path('activities/', views.activities, name='activities'),
    path('meditation/', views.meditation_guide, name = 'meditation'),
    path('yoga/', views.yoga_guide, name = 'yoga'),
    path('breathing/', views.breathing_guide, name = 'breathing'),
    path('music/', views.music_player, name = 'music'),
    path('tictac/', views.tictactoe, name = 'tictactoe'),
    path('2048/', views.game_2048, name = '2048'),
    path('snake/', views.snake, name = 'snake'),
]
