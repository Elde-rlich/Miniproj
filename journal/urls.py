from django.urls import path
from . import views

# urlpatterns = [
#     path('list/', views.journal_list, name = 'journal_list'),
#     path('create/', views.journal_create, name = 'journal_create'),
#     path('detail/<int:pk>', views.journal_detail, name = 'journal_detail'),
# ]

urlpatterns = [
    path('', views.journal_list, name='journal_list'),
    path('<int:pk>/', views.journal_detail, name='journal_detail'),
    path('create/', views.journal_create, name='journal_create'),
]
