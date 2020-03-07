from django.contrib import admin

from .models import (
    Product, Manufacturer, Material, Type, DesignDetail, CategoryDesignDetail, CategoryType, CategoryMaterial
)


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
admin.site.register(Material)
admin.site.register(Type)
admin.site.register(DesignDetail)
admin.site.register(CategoryMaterial)
admin.site.register(CategoryType)
admin.site.register(CategoryDesignDetail)

