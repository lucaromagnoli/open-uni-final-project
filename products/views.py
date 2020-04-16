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


def load_types(request):
    print(request)
    category_id = request.GET.get('category')
    types = CategoryType.objects.filter(category_id=category_id)
    return render(request, 'types_dropdown_list_options.html', {'types': types})
