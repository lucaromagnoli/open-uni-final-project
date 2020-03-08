from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import format_html


class Manufacturer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    website = models.URLField()
    city = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class DesignDetail(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class CategoryDesignDetail(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    design_detail = models.ForeignKey(DesignDetail, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.name} | {self.design_detail.name}'

    def validate_unique(self, exclude=None):
        obj = CategoryDesignDetail.objects.filter(category_id=self.category.id, design_detail_id=self.design_detail.id)
        if obj.exists():
            raise ValidationError(
                f'{type(self).__name__} {self.category.name} | {self.design_detail.name} already exist!')


class CategoryMaterial(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.name} | {self.material.name}'

    def validate_unique(self, exclude=None):
        obj = CategoryMaterial.objects.filter(category_id=self.category.id, material_id=self.material.id)
        if obj.exists():
            raise ValidationError(
                f'{type(self).__name__} {self.category.name} | {self.material.name} already exist!')


class CategoryType(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.name} | {self.type.name}'

    def validate_unique(self, exclude=None):
        obj = CategoryType.objects.filter(category_id=self.category.id, type_id=self.type.id)
        if obj.exists():
            raise ValidationError(f'{type(self).__name__} {self.category.name} | {self.type.name} already exist!')


class ProductGroup(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)


class Product(models.Model):
    GENDER_CHOICES = [
        ('M', 'men'),
        ('N', 'neutral'),
        ('W', 'women')
    ]

    title = models.CharField(max_length=200)
    product_url = models.URLField(max_length=200, unique=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(
        CategoryType, on_delete=models.CASCADE, null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True)
    design_details = models.ManyToManyField(CategoryDesignDetail)
    materials = models.ManyToManyField(CategoryMaterial)
    sku = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    currency = models.CharField(max_length=4, blank=True)
    dimensions = models.CharField(max_length=200, blank=True)
    weight = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.title} | {self.manufacturer} | {self.category}'

    def get_images(self):
        return (p.name for p in self.productimage_set.all())

    @staticmethod
    def image_path(name):
        return f'https://rossi-rei-data.s3.us-east-2.amazonaws.com/manufacturers/pictures/full/{name}'

    def product_images(self):
        """Method to return store image for admin panel"""

        images = ''
        for img in self.get_images():
            images += f'<img src="{self.image_path(img)}" height="300" width="300"/>'
        return format_html("".join(images))


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
