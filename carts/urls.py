from django.urls import path
from . import views
from addresses import views as address_view

app_name = 'cart'
urlpatterns = [
	path('', views.cart_home, name='home'),
	path('checkout', views.checkout_home, name='checkout'),
	path('checkout/address/create', address_view.checkout_address_create, name='checkout_create'),
	path('update', views.update_cart, name='update'),

]