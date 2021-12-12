from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import UserBase


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label='Enter username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required',
                             error_messages={'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email')

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name').lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError('Username Already exists')
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Passwords do not match.')
        return cd.get('password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email, that is already token')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Username',
            'id': 'login-username'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd'
        }
    ))
