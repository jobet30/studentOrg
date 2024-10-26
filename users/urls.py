from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_profile, name='user_profile'),
    path('<int:pk>/edit/', views.update_profile, name='update_profile')
]