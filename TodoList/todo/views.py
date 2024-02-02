from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from .forms import SignupForm, LoginForm, AddForm
from .utils import today
from .models import Category, Todo

# Create your views here.

def get_user_instance(request):
    return request.user

def get_user_todos(request):
    user = get_user_instance(request)
    user_todos = Todo.objects.filter(user = user)\
                             .filter(category = get_category(request))\
                             .order_by('-created_at')
    return user_todos

def get_user_todos_count(request):
    count = get_user_todos(request).count()
    return count

def get_completed_todos(request):
    output = get_user_todos(request).filter(completed = True)
    return output

def get_category(request):
    data = request.GET.get('category')[0].upper() + request.GET.get('category')[1:]
    category = Category.objects.get(name = data)
    return category

def get_percent_todo(request):
    todos = get_user_todos(request)
    completed_todos = get_completed_todos(request).count()
    todos_count_raw = todos.count()
    todos_count = 0
    if todos_count_raw < 1:
        todos_count = 1
    else:
        todos_count = todos_count_raw
    percent = int((completed_todos / todos_count) * 100)
    return percent
    
def common_data(request):
    percent = get_percent_todo(request)
    completed_todos = get_completed_todos(request).count()
    todos_count = get_user_todos_count(request)
    output = {
        'percent' : percent,
        'completed_todos' : completed_todos,
        'todos_count' : todos_count
    }
    return output

@login_required
def home(request):
    user = get_user_instance(request)
    date = today()
    todos = Todo.objects.filter(user = user)
    business_todos = todos.filter(category = 1).count()
    personal_todos = todos.filter(category = 2 ).count()
    health_todos = todos.filter(category = 3).count()
    shopping_todos = todos.filter(category = 4).count()
    incomplete_todos = todos.filter(completed = False).count()
    context = {
        'user' : user,
        'date' : date,
        'incomplete_todos' : incomplete_todos,
        'business_todos' : business_todos,
        'personal_todos' : personal_todos,
        'health_todos': health_todos,
        'shopping_todos' : shopping_todos
    }
    
    return render(request, 'todo/templates/home.html', context)
    
# CRUD Features : add, read, update, delete
    
class AddView(LoginRequiredMixin, View):
    model = Todo
    template_name = 'add.html'
    success_url = 'todo:home' 
    redirect_field_name = 'todo:login'
    
    def get(self, request):
        form = AddForm()
        return render(request, 
                      self.template_name, 
                      {
                          'form' : form,
                      })
    
    def post(self, request):
        form = AddForm(request.POST)
        user = get_user_instance(request)
        if form.is_valid():
            cd = form.cleaned_data
            todo_input = cd['todo_input']
            raw_category = cd['category']
            category = Category.objects.get(name = raw_category)
            todo = Todo.objects.create(
                title = todo_input,
                completed = False,
                category = category,
                user = user
            )
            todo.save()
            return redirect(self.success_url)
        return render(request, 'todo/templates/add.html', {'form' : form})

# detail of a todo

@login_required
def detail_todo(request):
    category = get_category(request)
    date = today()
    return render(request, 
                  'todo/templates/detail.html', 
                  {
                      'category_title' : category,
                      'date' : date,
                  }
                 )

@login_required
def list_todo(request):
    option = ""
    todos = []
    options = {
        '1' : get_user_todos(request),
        '2' : get_user_todos(request).filter(completed = False),
        '3' : get_user_todos(request).filter(completed = True)
    }
    if request.method == 'POST':
        option = request.POST.get('option')
        user_todos = options[option]
    for todo in user_todos:
        todos.append(
            {
                'title' : todo.title, 
                'completed' : todo.completed,
                
            }
        )
    response = dict(common_data(request), todos=todos)
    return JsonResponse(response, safe = False)
    
    
@login_required
def check_todo(request):
    if request.method == 'POST':
        todo_title = request.POST.get('text')
        done_str = request.POST.get('todoIsDone')
        done = True if done_str == 'true' else False
        todo = get_user_todos(request).filter(title = todo_title)
        todo.update(completed = done)
    return JsonResponse(common_data(request), safe = False)

@login_required
def delete_todo(request):
    if request.method == 'POST':
        todo_title = request.POST.get('text')
        todo = get_user_todos(request).filter(title = todo_title)
        todo.delete()
    return JsonResponse(common_data(request))

# User registration and authentication

class Signup(View):
    model = User 
    template_name = 'signup.html'
    success_url = 'todo:login'
    
    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, self.template_name, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, self.template_name, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['password']
                )
                user.save()    
            return redirect(self.success_url)
        return render(request, self.template_name, {'form' : form})

class Login(View):
    model = User
    template_name = 'login.html'
    success_url = 'todo:home'
    
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('todo:home')
        form = LoginForm()
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(username = username, password = password)
            if user:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                return redirect(self.success_url)    
            else:
                return render(request, 
                              self.template_name, 
                              {    
                                   'form' : form,
                                   'error_message' : 'incorrect username or password ! '
                              })

        return render(request, self.template_name, {'form' : form})

def signout(request):
    logout(request)
    return render(request, "todo/templates/logout.html")


