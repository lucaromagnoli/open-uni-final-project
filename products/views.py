from django.shortcuts import render
from django.db.models import Q
import django_filters

from .models import Product, CategoryType


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='iexact')
    type = django_filters.ModelChoiceFilter(queryset=CategoryType.objects.none())

    class Meta:
        model = Product
        fields = ('manufacturer', 'gender', 'category', 'type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.data.get('category'):
            category_id = int(self.data['category'])
            try:
                self.filters['type'].queryset = CategoryType.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass


def load_types(request):
    print(request)
    category_id = request.GET.get('category')
    types = CategoryType.objects.filter(category_id=category_id)
    return render(request, 'types_dropdown_list_options.html', {'types': types})


def product_list(request):
    f = ProductFilter(request.GET, queryset=Product.objects.all())
    return render(request, 'product_list.html', {'filter': f})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})
