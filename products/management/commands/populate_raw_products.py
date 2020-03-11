import urllib.parse
import ast

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd


from products import models


class Command(BaseCommand):
    help = 'Populate raw product from the scraper data set'
    gender_lookup = {
        'men': 'M',
        'neutral': 'N',
        'women': 'W'
    }

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
            required=False,
            default=None
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
    def get_materials(category, materials):
        mat_objs = []
        if isinstance(materials, str):
            for m in materials.split(','):
                try:
                    mat_objs.append(
                        models.CategoryMaterial.objects.get(category_id=category.id, material__name=m)
                    )
                except ObjectDoesNotExist:
                    continue
            return mat_objs

    @staticmethod
    def get_design_details(category, design_details):
        dd_objs = []
        if isinstance(design_details, str):
            for d in design_details.split(','):
                try:
                    dd_objs.append(
                        models.CategoryDesignDetail.objects.get(category_id=category.id, design_detail__name=d)
                    )
                except ObjectDoesNotExist:
                    continue
            return dd_objs

    @staticmethod
    def get_type(category, ptype):
        if isinstance(ptype, str):
            try:
                return models.CategoryType.objects.get(category_id=category.id, type__name=ptype)
            except ObjectDoesNotExist:
                return None
            except Exception as e:
                print(e)
                print(category, ptype)
                raise

    @staticmethod
    def get_images(images):
        img_list = []
        for img in ast.literal_eval(images):
            img_list.append(img['path'].replace('full/', ''))
        return img_list

    @staticmethod
    def get_manufacturer(manuf_name, website):
        try:
            return models.Manufacturer.objects.get(name=manuf_name)
        except ObjectDoesNotExist:
            manufacturer = models.Manufacturer(name=manuf_name, website=website)
            manufacturer.save()
            return manufacturer

    @transaction.atomic
    def _populate(self, df, manufacturer, cat_name):
        for row in df.itertuples():
            if getattr(row, 'category', None) is not None:
                category = models.Category.objects.get(name=row.category)
            else:
                category = models.Category.objects.get(name=cat_name)
            ptype = getattr(row, 'type', None)
            color = getattr(row, 'color', None)
            gender = getattr(row, 'gender', None)
            product = models.Product(
                title=row.name,
                category=category,
                product_url=row.url,
                manufacturer=manufacturer,
                gender=self.gender_lookup.get(gender),
                type=self.get_type(category, ptype) if ptype else None,
                description=row.description if row.description else '',
                currency=row.currency if row.currency else '',
                price=row.price if row.price else None,
                color=self.get_color(color) if color else None ,
                dimensions=row.dimensions if row.dimensions else '',
                weight=row.weight if row.weight else '',
                sku=row.sku if row.sku else '',
            )
            product.save()
            material = getattr(row, 'material', None)
            if material is not None:
                product.materials.set(self.get_materials(category, material))
            design_details = getattr(row, 'design_details', None)
            if design_details is not None:
                product.design_details.set(self.get_design_details(category, design_details))
            models.ProductImage.objects.bulk_create([
                models.ProductImage(product=product, name=name) for name in self.get_images(row.images)
            ])
            print(product)

    def handle(self, *args, **options):
        filename = options['file']
        try:
            df = pd.read_csv(
                f's3://rossi-rei-data/manufacturers/data/{filename}',
                encoding='utf-16',
                sep='\t',
                engine='python').fillna('')
        except UnicodeError:
            df = pd.read_csv(f's3://rossi-rei-data/manufacturers/data/{filename}').fillna('')
        website = self.get_manufacturer_website(df['url'][0])
        manufacturer = self.get_manufacturer(options['manufacturer'], website)
        self._populate(df, manufacturer, options['category'])
        print('done')
