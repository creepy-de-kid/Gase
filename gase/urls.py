from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from products.views import ProductListView, product_list_view

urlpatterns = [
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('products/', include('products.urls', namespace='products')),
    path('search/', include('search.urls')),
    path('cart/', include('carts.urls', namespace='cart')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)