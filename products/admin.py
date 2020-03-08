from django import forms
from django.contrib import admin

from .models import (
    Product, Manufacturer, Material, Type, DesignDetail, CategoryDesignDetail, CategoryType, CategoryMaterial
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['type', 'design_details', 'materials']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = CategoryType.objects.filter(
            category_id=self.instance.category_id)
        self.fields['design_details'].queryset = CategoryDesignDetail.objects.filter(
            category_id=self.instance.category_id)
        self.fields['materials'].queryset = CategoryMaterial.objects.filter(
            category_id=self.instance.category_id)


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    fields = (
        'title',
        'product_images',
        'gender',
        'category',
        'color',
        'type',
        'design_details',
        'materials'
    )
    readonly_fields = ('title', 'product_images')
    list_filter = ('manufacturer', 'category')


admin.site.register(Product, ProductAdmin)
admin.site.register(Manufacturer)
admin.site.register(Material)
admin.site.register(Type)
admin.site.register(DesignDetail)
admin.site.register(CategoryMaterial)
admin.site.register(CategoryType)
admin.site.register(CategoryDesignDetail)

