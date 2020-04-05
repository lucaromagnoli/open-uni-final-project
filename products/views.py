from django.shortcuts import render
from django.db.models import Q
import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['manufacturer', 'gender', 'category', 'type']


def index(request):
    context = {
        'queryset': 'qs'
    }

    return render(request, 'bootstrap_form.html', context)


def product_list(request):
    f = ProductFilter(request.GET, queryset=Product.objects.all())
    return render(request, 'template.html', {'filter': f})
