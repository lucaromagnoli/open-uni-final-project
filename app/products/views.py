from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views import View
import django_filters

from .models import Product, CategoryType
from .image_search import get_similar_products


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='iexact')
    type = django_filters.ModelChoiceFilter(queryset=CategoryType.objects.none())

    class Meta:
        model = Product
        fields = ('manufacturer', 'gender', 'category', 'type', 'design_details', 'materials')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.data.get('category'):
            category_id = int(self.data['category'])
            try:
                self.filters['type'].queryset = CategoryType.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass


@login_required()
def load_types(request):
    category_id = request.GET.get('category')
    types = CategoryType.objects.filter(category_id=category_id)
    return render(request, 'types_dropdown_list_options.html', {'types': types})


class SearchView(View):
    def get(self, request):
        return product_list_by_params(request)
    def post(self, request):
        return product_list_by_image(request)


def product_list_by_params(request):
    f = ProductFilter(request.GET, queryset=Product.objects.all().order_by('pk'))
    filtered_qs = f.qs
    paginator = Paginator(filtered_qs, 12)
    page = request.GET.get('page', '1')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    return render(
        request,
        'product_list.html',
        {'products': response, 'filter': f}
    )


def product_list_by_image(request):
    f = ProductFilter(request.GET, queryset=Product.objects.none())
    image_file = request.FILES['image_file']
    fs = FileSystemStorage()
    filename = fs.save(image_file.name, image_file)
    img_content = filename.read()
    rel_url = fs.url(filename)
    vectors = [
        (p.pk, p.image_vector) for p in Product.objects.all().order_by('pk')
    ]
    similar_pks = get_similar_products(img_content, vectors)
    similar_products = Product.objects.filter(pk__in=similar_pks)
    return render(
        request,
        'product_list.html',
        {'products': similar_products, 'filter': f, 'file_url': rel_url}
    )


@login_required()
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})
