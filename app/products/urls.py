from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import SearchView, product_detail, load_types, load_designdetails, load_materials

app_name = 'milaner'
urlpatterns = [
    path('products', login_required(SearchView.as_view()), name='product_list'),
    path('products/<int:pk>', product_detail, name='product_detail'),
    path('ajax/load-types/', load_types, name='ajax_load_types'),
    path('ajax/load-designdetails/', load_designdetails, name='ajax_load_designdetails'),
    path('ajax/load-materials/', load_materials,
         name='ajax_load_materials'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
