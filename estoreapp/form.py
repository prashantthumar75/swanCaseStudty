from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
# from .models import RegisterModel
from django import forms


class RegisterForm(forms.ModelForm):

    class Meta():
        model = get_user_model()
        fields = ['first_name','username', 'email', 'password']
        # fields = ['first_name','username', 'email', 'password1','password2']



class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')


