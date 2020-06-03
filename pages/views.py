from django.shortcuts import render

# from django.http import HttpResponse
from .forms import Contactform
from django.views.generic import TemplateView


def home_page(request):
  context = {
    'title':'Build something awesome',
    'content': 'Welcome to the home page.',
  }

  if request.user.is_authenticated:
   context['premium_content'] = 'Yeahhh'
   print(request.session.get('cart_id'))
   # print(request.session.get('user'))

  return render(request, 'pages/index.html', context)

def about_page(request):
  context = {
    'title':'about',
    'content': 'Welcome to the about page.'
  }

  return render(request, 'pages/index.html', context)

def contact_page(request):
  contact_form = Contactform(request.POST or None)

  if contact_form.is_valid():
    print(contact_form.cleaned_data)

  context = {
    'title':'Contact',
    'content': 'Welcome to the contact page.',
    'forms': contact_form,
    'brand': 'New brand name'
  }
  return render(request, 'pages/contact.html', context)

def login_page(request):
  return render(request, "auth/login.html")

def logout_page(request):
  return render(request, "auth/logout.html")

def register_page(request):
  return render(request, "auth/register.html")

class Bootstrap(TemplateView):
  template_name = "bootstrap/example.html"
