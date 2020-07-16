from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product
''' from django.db.models import Q ''' # Use as model

class SearchProductView(ListView):
	template_name = "search/view.html"

	def get_queryset(self, *args, **kwargs):
		request = self.request
		query = request.GET.get('q', None)
		# print(query)
		queryset_product = Product.objects

		if query != None:
			return queryset_product.q_lookup(query)
		else:
			return queryset_product.featured()

	def get_context_date(self, *args, **kwargs):
		context = super(SearchProductView, self).get_context_date(*args, **kwargs)
		query = self.request.Get.get('get')
		context['query'] = query
		# SearchQuery.objects.create(query=query)
		return context
