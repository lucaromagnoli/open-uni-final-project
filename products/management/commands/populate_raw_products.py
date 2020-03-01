import urllib.parse
import ast

from django.core.management.base import BaseCommand
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd


from products import models


class Command(BaseCommand):
    help = 'Populate raw product from the scraper data set'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            help='The s3 file to read data from',
            required=True
        )
        parser.add_argument(
            '--manufacturer',
            help='The name of the manufacturer',
            required=True
        )
        parser.add_argument(
            '--category',
            help='The category of the products',
            required=True
        )

    @staticmethod
    def get_manufacturer_website(product_url):
        parts = urllib.parse.urlparse(product_url)
        return urllib.parse.urlunparse((parts.scheme, parts.netloc, '', '', '', ''))

    @staticmethod
    def get_color(color):
        try:
            return models.Color.objects.get(name=color)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_materials(materials):
        mat_objs = []
        for m in materials.split(','):
            try:
                mat_objs.append(models.Material.objects.get(name=m.split().lower()))
            except ObjectDoesNotExist:
                continue
        return mat_objs

    @staticmethod
    def get_images(images):
        img_list = []
        for img in ast.literal_eval(images):
            img_list.append(img['path'].replace('full', ''))
        return img_list

    @transaction.atomic
    def _populate(self, filename, manuf_name, cat_name):
        df = pd.read_csv(filename)
        website = self.get_manufacturer_website(df['url'][0])
        manufacturer = models.Manufacturer(name=manuf_name, website=website)
        manufacturer.save()
        category = models.Category.objects.get(name=cat_name)
        for row in df.itertuples():
            product = models.Product(
                title=row.name,
                category=category,
                product_url=row.url,
                manufacturer=manufacturer,
                description=row.description if row.description else '',
                currency=row.currency if row.currency else '',
                price=row.price if row.price else None,
                color=self.get_color(row.color),
                dimensions=row.dimensions if row.dimensions else '',
                weight=row.weight if row.weight else '',
                sku=row.sku if row.sku else '',
            )
            product.save()
            product.materials.set(self.get_materials(row.material))
            models.ProductImage.objects.bulk_create([
                models.ProductImage(product=product, name=name) for name in self.get_images(row.images)
            ])

    def handle(self, *args, **options):
        self._populate(options['file'], options['manufacturer'], options['locale'])
        print('done')
