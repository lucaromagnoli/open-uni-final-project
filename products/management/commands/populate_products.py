import ast

from babel.numbers import parse_decimal
from django.core.management.base import BaseCommand
from django.db import transaction
import pandas as pd


from products import models


class Command(BaseCommand):
    help = 'Populate Products from file'
    gender_lookup = {
        'men': 'M',
        'neutral': 'N',
        'women': 'W'
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            help='The file to read data from',
            required=True
        )
        parser.add_argument(
            '--manufacturer',
            help='The name of the manufacturer',
            required=True
        )
        parser.add_argument(
            '--locale',
            help='The locale for price decimal separators',
            default='it'
        )

    @transaction.atomic
    def _populate(self, filename, manuf_name, locale):
        def get_design_details_from_df():
            if row.design_details:
                return row.design_details.split(',')

        def get_details_objs(_category, _details):
            objs = []
            for d in _details:
                objs.append(models.CategoryDesignDetail.objects.get(category__name=_category, design_detail__name=d))
            return objs

        def get_materials_from_df():
            if row.material:
                return row.material.split(',')

        def get_material_objs(_category, _materials):
            objs = []
            for m in _materials:
                objs.append(models.CategoryMaterial.objects.get(category__name=_category, material__name=m))
            return objs

        df = pd.read_csv(filename).fillna('')
        print(manuf_name)
        manufacturer = models.Manufacturer.objects.get(name=manuf_name)
        groups = df.groupby('group')
        for k, v in groups:
            product_group = models.ProductGroup(manufacturer=manufacturer)
            product_group.save()
            for row in v.itertuples():
                try:
                    images = [img['path'] for img in ast.literal_eval(row.images)]
                    design_details = get_design_details_from_df()
                    materials = get_materials_from_df()
                    category = models.Category.objects.get(name=row.category) if row.category else None
                    product = models.Product(
                        title=row.title,
                        product_url=row.url,
                        manufacturer=manufacturer,
                        gender=self.gender_lookup.get(row.gender, 'N'),
                        category=category,
                        type=models.CategoryType.objects.get(type__name=row.type, category__name=row.category) if row.type else None,
                        color=models.Color.objects.get(name=row.color.split(',')[0]) if row.color else None,
                        sku=row.sku if row.sku else None,
                        price=parse_decimal(row.price, locale=locale) if row.price else None,
                        currency=row.currency if row.currency else None,
                        dimensions=row.dimensions if row.dimensions else None,
                        weight=row.weight if row.weight else None,
                        group=product_group if product_group else None
                    )
                    product.save()
                    if design_details:
                        product.design_details.set(get_details_objs(row.category, design_details))
                    if materials:
                        product.materials.set(get_material_objs(row.category, materials))
                    print(f'product saved: {product}')
                    models.ProductImage.objects.bulk_create([
                        models.ProductImage(product=product, name=name) for name in images
                    ])
                    print('saved images')
                except Exception as e:
                    print(e)
                    print(row)
                    raise

    def handle(self, *args, **options):
        self._populate(options['file'], options['manufacturer'], options['locale'])
        print('done')
