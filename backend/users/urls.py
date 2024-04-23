from django.urls import path
from . import views

urlpatterns =[
    path('api/user/', views.CustomUserDetailView.as_view(), name='user-detail'),


]