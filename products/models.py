from django.core.exceptions import ValidationError
from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField()
    city = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class DesignDetail(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CategoryType(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category}| {self.type}'


class CategoryDesignDetail(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    design_detail = models.ForeignKey(DesignDetail, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category} | {self.design_detail}'


class Material(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Product(models.Model):
    GENDER_CHOICES = [
        ('M', 'men'),
        ('N', 'neutral'),
        ('W', 'women')
    ]
    title = models.CharField(max_length=200)
    unique_id = models.CharField(max_length=32)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_types = models.ManyToManyField(CategoryType)
    design_details = models.ManyToManyField(CategoryDesignDetail)
    colors = models.ManyToManyField(Color)
    materials = models.ManyToManyField(Material)
    sku = models.CharField(max_length=20, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    currency = models.CharField(max_length=4, blank=True)
    dimensions = models.CharField(max_length=20, blank=True)
    weight = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.title} | {self.manufacturer} | {self.category}'

    def clean(self):
        for t in self.product_types.objects.all():
            if t.category != self.category:
                raise ValidationError(f'Invalid product type: {t} for product with category {self.category}')
        for d in self.design_details.objects.all():
            if self.category != d.category:
                raise ValidationError(f'Invalid design detail: {d} for product with category {self.category}')


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
