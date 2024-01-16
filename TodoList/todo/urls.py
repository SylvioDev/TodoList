from django.urls import path 
from . import views
from .views import home

app_name = 'todo'

urlpatterns = [
    path('home/', views.home, name = "homepage")
]