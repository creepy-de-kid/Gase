from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save

import os
import random
from gase.utils import unique_slug_generator

''' Renaming files for media path '''

def get_file_ext(filepath):
  base_name = os.path.basename(filepath)
  name, ext = os.path.splitext(base_name)

  return name, ext

def uplaod_image_path(instannce, filename):
  new_filename = random.randint(1, 3999456235)
  name, ext = get_file_ext(filename)
  final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)

  return 'product/{new_filename}/{final_filename}'.format(new_filename=new_filename, final_filename=final_filename)

''' Renaming files for media path '''

# Custom queryset
class ProductQuerySet(models.query.QuerySet):
  def featured(self):
    return self.filter(featured=True)

  def active(self):
    return self.filter(active=True)

  def q_lookup(self, query):
    lookups = (
      Q(title__icontains=query) | 
      Q(description__icontains=query) | 
      Q(price__icontains=query) |
      Q(tag__title__icontains=query)
    )
    return self.filter(lookups).distinct()

'''Custom manager for class views '''
class ProductManager(models.Manager):
  def get_queryset(self):
    return ProductQuerySet(self.model, self._db)

  # Overrides all() call by not get active project whem set to false
  def all(self):
    return self.get_queryset().active()

   # Bind method to search Product objects models:
  def features(self):
    featured = self.get_queryset().featured()

    return featured

  def q_lookup(self, query):
    q_lookup = self.get_queryset().q_lookup(query)

    return q_lookup


  def get_by_id(self, id):
    qs = self.get_queryset().filter(pk = id) # self.get_queryset() == Product.objects
    
    if qs.count() == 1:  
      return qs.first()
    
    return None
'''Custom manager ends '''

class Product(models.Model):
  title = models.CharField(max_length=100)
  slug = models.SlugField(default='abc', blank=True, unique=True)
  description = models.TextField()
  price = models.DecimalField(decimal_places=2, default=200.99, max_digits=19)
  image = models.ImageField(upload_to=uplaod_image_path, null=True, blank=True)
  featured = models.BooleanField(default=False)
  active = models.BooleanField(default=True)
  timestamp = models.DateField(auto_now_add=True)

  # Binding custom model manager objects
  objects = ProductManager()

  # Get product absolute url
  """ def get_absolute_url(self):
    #  return "/product/{slug}/".format(slug = self.slug)
    return reverse('products:detail', kwargs={'slug': self.slug}) """

  def __str__(self):
    return self.title

# Signal function
def product_pre_save_reciever(sender, instance, *args, **kwargs):
  if not instance.slug:
    instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_reciever, sender=Product) # Django signal