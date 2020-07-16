from django.shortcuts import render, redirect

from . import forms
from .models import Guest
from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.utils.http import is_safe_url

def guest_register(request):
  form = forms.GuestForm(request.POST or None)

  
  next_post = request.POST.get('next')
  next_get = request.GET.get('next')

  redirect_path = next_post or next_get
  print(redirect_path)

  context = {
    'forms': form
  }

  if form.is_valid():
    email = form.cleaned_data['email']
    new_guest_email = Guest.objects.create(email=email)
    request.session['guest_email_id'] = new_guest_email.id
    if is_safe_url(redirect_path, request.get_host(), require_https=False):
      return redirect(redirect_path)
    else:
      return redirect('accounts:register')
  return redirect('accounts:register')

def login(request):
  form = forms.LoginForm(request.POST or None)

  next_get = request.GET.get('next')
  next_post = request.POST.get('next')
  redirect_path = next_get or next_post or None

  context = {
    'forms': form
  }

  if form.is_valid():
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
      try:
        del  request.session['guest_email_id']
      except:
        pass
      auth_login(request, user)
      # [TODO] Make sure user get redirect to checkout when login in checkout
      if is_safe_url(redirect_path, request.get_host()):
        return redirect(redirect_path)
      else:
        return redirect('/')
    else:
      # Return an invalid error message
      print('Error')
  
  return render(request, 'auth/login.html', context)

def user_logout(request):
  logout(request)
  # [TODO] Redirect back to login
  return redirect('/')


def register(request):
  form = forms.RegisterForm(request.POST or None)
  user = get_user_model()

  if form.is_valid():
    username = form.cleaned_data['username']
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    new_user = user.objects.create_user(username, email, password)

  context = {
    'forms': form
  }
  return render(request, 'auth/register.html', context)
