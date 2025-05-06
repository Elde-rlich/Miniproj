from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='chatbot'),
    path('api/chatbot/', views.ChatbotAPI.as_view(), name='chatbot_api'),
]