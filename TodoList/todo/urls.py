from django.urls import path 
from . import views
from .views import home, Signup, Login, signout, AddView, detail_todo, list_todo, check_todo, delete_todo
app_name = 'todo'

urlpatterns = [
    path('home/', views.home, name = "home"),
    path('signup/', views.Signup.as_view(), name = "signup"),
    path('login/', views.Login.as_view(), name = "login"),
    path('logout/', views.signout, name = "logout"),
    path('add/', views.AddView.as_view(), name = 'add'),
    path('list/', views.detail_todo, name = 'todo-list'),
    path('todos/', views.list_todo, name = 'todos'),
    path('check/', views.check_todo, name = 'check'),
    path('delete/', views.delete_todo, name = 'delete')
]

