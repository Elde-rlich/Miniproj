from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from allauth.socialaccount.providers.google.urls import urlpatterns as google_urls

urlpatterns =[
    path('register/', views.register, name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name = 'authapp/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'authapp/logout.html'), name = 'logout'),
    #path('home/', views.home, name = 'home'),
    path('pswd_reset/', auth_views.PasswordResetView.as_view(template_name = 'authapp/password_reset.html'), name = 'password_reset'),
    path('pswd_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = 'authapp/password_reset_done.html'), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name= 'authapp/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name= 'authapp/password_reset_complete.html'), name='password_reset_complete'),
    path('accounts/', include('allauth.urls')),
    #*google_urls,
]