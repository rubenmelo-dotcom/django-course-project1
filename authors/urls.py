from django.urls import path
from django.shortcuts import render
from . import views


urlpatterns = [
    path('register/', views.register_view, name='register')
]
