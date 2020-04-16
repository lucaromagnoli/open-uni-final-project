from django.urls import path
from django_filters.views import FilterView

from .views import product_list, load_types

app_name = 'milaner'
urlpatterns = [
    path('products', product_list),
    path('ajax/load-types/', load_types, name='ajax_load_types'),
]
