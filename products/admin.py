from django.contrib import admin

from .models import Product, Manufacturer


class ProductAdmin(admin.ModelAdmin):
    fields = (
        'title',
        'product_images',
        'gender',
        'category',
        'type',
        'color',
        'design_details',
        'materials'
    )
    readonly_fields = ('title', 'product_images')


admin.site.register(Product, ProductAdmin)
admin.site.register(Manufacturer)
