import random
import string

from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
	return "".join(random.choice(chars) for _ in range(size))


# Generate random string for order_id model field
def unique_order_id_generator(instance):
	new_order_id = random_string_generator()

	klass = instance.__class__
	qs_exists = klass.objects.filter(order_id=new_order_id).exists()

	if qs_exists:
		return unique_order_id_generator(instance)
	return new_order_id

# Generate random string for slug model field
def unique_slug_generator(instance, new_slug=None):
	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(instance.title)

	klass = instance.__class__
	qs_exists = klass.objects.filter(slug=slug).exists()

	if qs_exists:
		new_slug = "{slug}-{randstr}".format(
			slug=slug, 
			randstr=random_string_generator(size=4)
		)

		return unique_slug_generator(instance, new_slug=new_slug)
	return slug