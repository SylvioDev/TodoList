from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import SignupForm, LoginForm

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'todo/templates/home.html', 
                      {
                          'user' : user
                      })
    else:
        return redirect('todo:login')
    
class Signup(View):
    model = User 
    template_name = 'signup.html'
    success_url = 'login'
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
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.save()    
            return redirect('todo:login')
        return render(request, self.template_name, {'form' : form})

class Login(View):
    model = User
    template_name = 'login.html'
    success_url = 'todo:home'
    def get(self, request):
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
