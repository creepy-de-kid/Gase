from django.urls import path
from . import views


urlpatterns = [
  path("", views.home_page, name="home"),
  path("about", views.about_page, name="about"),
  path('contact', views.contact_page, name="contact"),
  path('login', views.login_page, name="login"),
  path('logout', views.logout_page, name="logout"),
  path('register', views.register_page, name="register"),
  path('bootstrap', views.Bootstrap.as_view(), name="bootstrap"),
]
