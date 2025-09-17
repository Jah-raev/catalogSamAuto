from django import forms
# from .models import Clients, Employees, Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class AuthLoginForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(forms.ModelForm):
        password = forms.CharField(label='Password', widget=forms.PasswordInput)
        password2 = forms.CharField(label='Repeat password input!', widget=forms.PasswordInput)

        class Meta:
            model = User
            fields = ['username', 'first_name', 'email']

        def clean_password2(self):
                cd = self.cleaned_data
                if cd['password'] != cd['password2']:
                    raise forms.ValidationError('password don\'t match.')
                return cd['password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email' )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('department', 'position', 'phoneNumber')
