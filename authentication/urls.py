from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('email_confirmation/', views.send_email_confirmation, name='email_confirmation'),
]
