from django.urls import path
from . import views

urlpatterns = [
    path('', views.settings_main, name = 'settings_main'),
    
]