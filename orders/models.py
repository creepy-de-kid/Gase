from django.db import models

import math
from carts.models import Cart
from gase.utils import unique_order_id_generator
from billing.models import BillingProfile
from addresses.models import Address

from django.db.models.signals import pre_save, post_save

ORDER_STATUS_CHOICES = (
	('created', 'Created'),
	('shipped', 'Shipped'),
	('refunded', 'Refunded'),
	('paid', 'Paid'),
)

class OrderManager(models.Manager):

	def new_or_get(self, billing_profile, cart_obj):
		created = False
		qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True)
		if qs.count() >= 1:
			obj = qs.first()
		else:
			obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
			created  = True
		return obj, created

class Order(models.Model):
	order_id = models.CharField(max_length=120, blank=True)
	billing_profile = models.ForeignKey(BillingProfile, null=True, on_delete=models.CASCADE) 
	shipping_address = models.ForeignKey(Address, related_name="shipping_address", null=True, on_delete=models.CASCADE) 
	billing_address = models.ForeignKey(Address, related_name="billing_address", null=True, on_delete=models.CASCADE) 
	cart  = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
	status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
	shipping_total = models.DecimalField(default=1500, max_digits=100, decimal_places=2)
	total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	active = models.BooleanField(default=True)

	# Order manager objects
	objects = OrderManager()

	def __str__(self):
		return self.order_id

	# Generate the order total
	def update_total(self):
		cart_total = self.cart.total
		shipping_total = self.shipping_total
		order_total = math.fsum([cart_total, shipping_total])
		formatted_total = format(order_total, '.2f')
		self.total = formatted_total
		self.save()
		return order_total


# Generate the order id
def pre_save_create_order_id(sender, instance, *args, **kwargs):
	if not instance.order_id:
		instance.order_id = unique_order_id_generator(instance)
	qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
	if qs.exists():
		qs.update(active=False)
pre_save.connect(pre_save_create_order_id, sender=Order)

# if cart changed
def post_save_cart_total(sender, instance, created, *args, **kwargs):
	if not created:
		cart_obj = instance
		cart_total = cart_obj.total
		cart_id = cart_obj.id
		qs = Order.objects.filter(cart__id=cart_id)
		if qs.count() == 1:
			order_obj = qs.first()
			order_obj.update_total()
post_save.connect(post_save_cart_total, sender=Cart)

# Save order total if changed
def post_save_order(sender, instance, created=True, *args, **kwargs):
	# print('running')
	if created:
		print('updating..first')
		instance.update_total()
	print('updated')
post_save.connect(post_save_order, sender=Order)