from django.urls import path
from django_filters.views import FilterView

from .models import Product
from .views import product_list

app_name = 'milaner'
urlpatterns = [
    path('', product_list, name='index'),
]