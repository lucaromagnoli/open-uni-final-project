from django.urls import path
from django_filters.views import FilterView

from .views import ProductFilter, load_types

app_name = 'milaner'
urlpatterns = [
    path(
        '',
        FilterView.as_view(
            filterset_class=ProductFilter,
            template_name='search_form.html'),
        name='index'
    ),
    path('ajax/load-types/', load_types, name='ajax_load_types'),
]
