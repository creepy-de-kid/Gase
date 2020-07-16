from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import Http404

from .models import Product
from carts.models import Cart

# Featured view start
class ProductFeaturedListView(ListView):
  # queryset = Product.objects.all()
  template_name = "products/list.html"
  
  def get_queryset(self, *args, **kwargs):
    request = self.request

    return Product.objects.all().featured()

class ProductFeaturedDetailView(DetailView):
  template_name = "products/featured-detail.html"

  def get_queryset(self, *args, **kwargs):
    request = self.request
    # pk = self.kwargs.get('pk');
    qs = Product.objects.all().featured()#.filter(pk = pk)
    
    return qs
    
  def get_context_data(self, *args, **kwargs):
    # base implentation to get context
    context = super(ProductFeaturedDetailView, self).get_context_data(**kwargs)
    # Add in query set of all Product
    # context['detail'] = self.get_queryset()
    print(context)
    return context
# Featured view end

class ProductListView(ListView):
  queryset = Product.objects.all()
  template_name = "products/list.html"

  def get_context_data(self, *args, **kwargs):
    # base implentation to get context
    context = super(ProductListView, self).get_context_data(**kwargs)
    # Add in query set of all Product
    context['object_list'] = self.queryset

    return context


def product_list_view(request):
  queryset = Product.objects.all()

  context = {
    "object_list": queryset
  }
  
  return render(request, "products/list.html", context)

class ProductDetailSlugView(DetailView):
  template_name = "products/detail.html"
  queryset = Product.objects.all()

  def get_object(self, *args, **kwargs):
    request = self.request
    slug = self.kwargs.get('slug')

    try:
      instance = get_object_or_404(Product, slug=slug, active=True)
    except Product.DoesNotExist:
      raise Http404("Product not found..")
    except Product.MultipleObjectsReturned:
      qs = Product.objects.filter(slug=slug, active=True)

      instance = qs.first()
      return instance
    except:
      raise Http404('Oops! Something has gone wrong.')


    if instance == None:
      raise Http404('Product does not exist')

    return instance

  def get_context_data(self, *args, **kwargs):
    request = self.request
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = super().get_context_data(*args, **kwargs)
    context['cart'] = cart_obj
    context['detail'] = self.get_object()
    return context

def product_detail_view(request, detail_id):
  # Returns a 404 page if not found
  # instance = get_object_or_404(Product, pk=detail_id, featured=True)
  # Return error if not found

  """ try:
    instance = Product.objects.get(pk=detail_id, featured=True)
  except Product.DoesNotExist:
    print('No such product')
    raise Http404('Product does not exist')
  except:
    print('Huh?') """
  
  instance = Product.objects.get_by_id(id = detail_id)

  if instance == None:
    raise Http404('Product does not exist')



  """ qs = Product.objects.filter(pk=detail_id)
  print(qs)

  if qs.exists() and qs.count() == 1:
    instance = qs.first()
  else:
    raise Http404("Product does exist") """

  context = {
    "detail": instance
  }
  return render(request, "products/detail.html", context)
