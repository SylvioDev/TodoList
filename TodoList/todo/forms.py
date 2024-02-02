from django import forms
from .models import Category

class SignupForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput(
        attrs = {
            "class" : "inputs data",
            "placeholder" : "username"
        }
    ))

    password = forms.CharField(widget = forms.PasswordInput(
        attrs = {
            "class" : "inputs data",
            "placeholder" : "password"
        }
    ))
    
    password_repeat = forms.CharField(widget = forms.PasswordInput(
        attrs = {
            "class" : "inputs data",
            "placeholder" : "repeat password"
        }
    ))

class LoginForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput(
        attrs = {
            "class" : "inputs data",
            "placeholder" : "username"
        }
    ))

    password = forms.CharField(widget = forms.PasswordInput(
        attrs = {
            "class" : "inputs data",
            "placeholder" : "password"
        }
    ))

    remember_me = forms.BooleanField(required = False)

CATEGORIES = [
    ('Business', 'Business'),
    ('Personal', 'Personal'),
    ('Health', 'Health'),
    ('Shopping', 'Shopping')
]

class AddForm(forms.Form):
    todo_input = forms.CharField(widget = forms.TextInput(
        attrs = {
            'placeholder' : 'e.g Get some milk',
            'id' : 'content'
        }
    ))
        
    category = forms.CharField(label = '', widget = forms.Select(
        choices = CATEGORIES,
        attrs = {
            'class' : 'form-select'
        }
        ))
    
