from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import ShippingAddress,Profile
from django import forms


class RegisterForm(forms.ModelForm):

    class Meta():
        model = get_user_model()
        fields = ['first_name','username', 'email', 'password']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')


class ProfileFrom(forms.ModelForm):

    class Meta():
        model = Profile
        fields = "__all__"


class ShippingAddressFrom(forms.ModelForm):

    class Meta():
        model = ShippingAddress
        fields = "__all__"
