from django import forms
from django.contrib import admin
from django.http import QueryDict
from django.shortcuts import redirect


from .models import (
    Product, Manufacturer, Material, Type, DesignDetail, CategoryDesignDetail,
    CategoryType, CategoryMaterial, Color
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


class GotoNextAdminMixin(object):

    # https://stackoverflow.com/questions/58014139/how-to-go-to-next-object-in-django-admin

    def get_next_instance_pk(self, request, current):
        """Returns the primary key of the next object in the query (considering filters and ordering).
        Returns None if the object is not in the queryset.
        """
        querystring = request.GET.get('_changelist_filters')
        if querystring:
            # Alters the HttpRequest object to make it function as a list request
            original_get = request.GET
            try:
                request.GET = QueryDict(querystring)
                # from django.contrib.admin.options: ModelAdmin.changelist_view
                ChangeList = self.get_changelist(request)
                list_display = self.get_list_display(request)
                changelist = ChangeList(
                    request,
                    self.model,
                    list_display,
                    self.get_list_display_links(request, list_display),
                    self.get_list_filter(request),
                    self.date_hierarchy,
                    self.get_search_fields(request),
                    self.get_list_select_related(request),
                    self.list_per_page,
                    self.list_max_show_all,
                    self.list_editable,
                    self,
                    self.sortable_by)
                queryset = changelist.get_queryset(request)
            finally:
                request.GET = original_get
        else:
            queryset = self.get_queryset(request)

        # Try to find pk in this list:
        iterator = queryset.values_list('pk', flat=True).order_by('-pk').iterator()
        try:
            while next(iterator) != current.pk:
                continue
            return next(iterator)
        except StopIteration:
            # Not found or it was the last item
            pass


class ProductAdmin(admin.ModelAdmin, GotoNextAdminMixin):
    # form = ProductForm
    # ordering = ['pk']
    fields = (
        'title',
        'product_url',
        'product_images',
        'gender',
        'category',
        'color',
        'type',
        'design_details',
        'materials'
    )
    readonly_fields = ('title', 'product_url', 'product_images')
    list_filter = ('manufacturer', 'category')

    def response_change(self, request, obj):
        """Determines the HttpResponse for the change_view stage."""
        if '_next_item' in request.POST:
            next_pk = self.get_next_instance_pk(request, obj)
            if next_pk:
                response = redirect('admin:products_product_change', next_pk)
                qs = request.GET.urlencode()  # keeps _changelist_filters
            else:
                # Last item (or no longer in list) - go back to list in the same position
                response = redirect('admin:products_product_changelist')
                qs = request.GET.get('_changelist_filters')

            if qs:
                response['Location'] += '?' + qs
            obj.save()
            return response
        return super().response_change(request, obj)


admin.site.register(Product, ProductAdmin)
admin.site.register(Manufacturer)
admin.site.register(Material)
admin.site.register(Color)
admin.site.register(Type)
admin.site.register(DesignDetail)
admin.site.register(CategoryMaterial)
admin.site.register(CategoryType)
admin.site.register(CategoryDesignDetail)
