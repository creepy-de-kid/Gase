from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class GuestForm(forms.Form):
  email_attrs = {
    'id': 'guest-email',
    'class':  'form-control',
    'placeholder': 'Enter email',
    'maxlength': '100'
  }
  
  email = forms.EmailField(widget=forms.EmailInput(attrs=email_attrs))

class LoginForm(forms.Form):
  username_attrrs = {
    'id': 'username',
    'class':  'form-control',
    'placeholder': 'Enter Username',
    'maxlength': '100'
  }

  password_attrrs = {
    'id': 'password',
    'class':  'form-control',
    'placeholder': 'Enter Password',
  }

  username = forms.CharField(widget=forms.TextInput(attrs=username_attrrs))
  password = forms.CharField(widget=forms.PasswordInput(attrs=password_attrrs))




class RegisterForm(forms.Form):
  username_attrs = {
    'id': 'username',
    'class':  'form-control',
    'placeholder': 'Enter Username',
    'maxlength': '100'
  }

  email_attrs = {
    'id': 'email',
    'class':  'form-control',
    'placeholder': 'Enter Email',
    'maxlength': '100'
  }

  password_attrs = {
    'id': 'password',
    'class':  'form-control',
    'placeholder': 'Enter Password',
  }

  password2_attrs = {
    'id': 'password2',
    'class':  'form-control',
    'placeholder': 'Enter Password',
  }

  username = forms.CharField(widget=forms.TextInput(attrs=username_attrs))
  email = forms.EmailField(label='email', widget=forms.EmailInput(attrs=email_attrs))
  password = forms.CharField(widget=forms.PasswordInput(attrs=password_attrs))
  password2 = forms.CharField(label='password2', widget=forms.PasswordInput(attrs=password2_attrs))

  def clean_username(self):
    username = self.cleaned_data.get('username')
    qs = User.objects.filter(username=username)

    if qs.exists():
      print('Username is taken')
      raise forms.ValidationError('Username is taken')
    return username
  
  def clean_email(self):
    email = self.cleaned_data.get('email')
    qs = User.objects.filter(email=email)

    if qs.exists():
      print('Email is taken')
      raise forms.ValidationError('Email is taken')
    return email

  def clean(self):
    data = self.cleaned_data
    password = self.cleaned_data.get('password')
    password2 = self.cleaned_data.get('password2')

    if password2 != password:
     raise forms.ValidationError('Password must match.')
    
    return data

  