from django import forms

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

    