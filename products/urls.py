from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
  path("", views.ProductListView.as_view(), name='products'),
  path("<slug:slug>", views.ProductDetailSlugView.as_view(), name="product_detail"),
]