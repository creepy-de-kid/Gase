from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
  path('login', views.login, name='login'),
  path('logout', views.user_logout, name='logout'),
  path('register', views.register, name='register'),
   path('register/guest', views.guest_register, name='guest_register')
]