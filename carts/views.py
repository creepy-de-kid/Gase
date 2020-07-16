from django.shortcuts import render, redirect
import django.db.utils as error_checker
from django.http import JsonResponse

from billing.models import BillingProfile
from products.models import Product
from orders.models import Order
from .models import Cart

from addresses.models import Address
from addresses.forms import AddressForm

from accounts.models import Guest
from accounts import forms

def cart_home(request):
	# Cart logic in written in model manger
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	cart_id = request.session.get('cart_id')
	cart = Cart.objects.get_object(cart_id)
	context = {
		'cart': cart,
	}
	return render(request, 'carts/home.html', context)

def update_cart(request):
	product_id = request.POST.get('product_id')
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print('Product is gone')
			return redirect('cart:home')

			# Adds item to cart
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if product_obj in cart_obj.product.all():
			cart_obj.product.remove(product_obj)
			product_added = False
		else:
			cart_obj.product.add(product_obj)
			product_added = True

		# Count item in cart
		request.session['cart_total'] = cart_obj.product.count()
		
		if request.is_ajax():
			cart_count = cart_obj.product.count()
			response = {
				'added': product_added,
				'removed': not product_added,
				'cartCount': cart_count
			}
			return JsonResponse(response)
	return redirect('cart:home')

def checkout_home(request):
	# Get cart and order
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	order_obj = None
	if cart_created or cart_obj.product.count() == 0:
		return redirect('cart:home')

	login_form = forms.LoginForm()
	guest_form = forms.GuestForm()
	address_form = AddressForm()

	billing_profile,billing_profile_created = BillingProfile.objects.new_or_get(request)
	billing_address_id = request.session.get('billing_address_id')
	shipping_address_id = request.session.get('shipping_address_id')
	print(billing_address_id, shipping_address_id)

	if billing_profile != None:
		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
		if shipping_address_id:
			order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
			del  request.session['shipping_address_id']
		if billing_address_id:
			order_obj.billing_address = Address.objects.get(id=billing_address_id)
			del  request.session['billing_address_id']
			order_obj.save()

	context = {
		'object': order_obj,
		'billing_profile': billing_profile,
		'guest_form': guest_form,
		'login_form': login_form,
		'address_form':address_form,
	}	

	return render(request, 'carts/checkout.html', context)
