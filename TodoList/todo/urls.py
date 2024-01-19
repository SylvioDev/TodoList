from django.urls import path 
from . import views
from .views import home, Signup, Login, signout
app_name = 'todo'

urlpatterns = [
    path('home/', views.home, name = "home"),
    path('signup/', views.Signup.as_view(), name = "signup"),
    path('login/', views.Login.as_view(), name = "login"),
    path('logout/', views.signout, name = "logout")
]

