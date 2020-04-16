from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import product_list, load_types

app_name = 'milaner'
urlpatterns = [
    path('products', product_list),
    path('ajax/load-types/', load_types, name='ajax_load_types'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
