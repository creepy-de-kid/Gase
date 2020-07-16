from django.db import models
from products.models import Product

from django.db.models.signals import pre_save, post_save
from gase.utils import unique_slug_generator

class Tag(models.Model):
	title = models.CharField(max_length=120)
	slug = models.SlugField()
	timestamp = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	# Tag relationship to product
	products = models.ManyToManyField(Product, blank=True)

	def __str__(self):
		return self.title

# Signal function
def tag_pre_save_reciever(sender, instance, *args, **kwargs):
  if not instance.slug:
    instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_reciever, sender=Tag) # Django signal
