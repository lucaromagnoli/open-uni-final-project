from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from products.views import product_list

urlpatterns = [
    # path('login/', auth_views.login, name='login'),
    # path('logout/', auth_views.logout, name='logout'),
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('', product_list, name='home')
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)