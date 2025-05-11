from django import forms
from .models import Staff

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'username', 'password', 'role']

    password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
