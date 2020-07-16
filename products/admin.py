from django.contrib import admin

from .models import Product

class ProductAdmin(admin.ModelAdmin):
	list_display = ('title', 'id', 'slug')

	class Meta:
		model = Product

# Register model into admin
admin.site.register(Product, ProductAdmin)
