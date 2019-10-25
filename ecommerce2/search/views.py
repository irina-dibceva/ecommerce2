from django.views.generic import ListView

from products.models import *


class SearchProductView(ListView):
    template_name = 'products/product_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchProductView, self).get_context_data()
        query = self.request.GET.get('q')
        context['query'] = query
        # SeachQuery.objects.create(query=query)
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.none()
