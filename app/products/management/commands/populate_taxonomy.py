import os

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.db import transaction


import pandas as pd

from products.models import (
    Category, Color, DesignDetail, Material, Type, CategoryType, CategoryMaterial, CategoryDesignDetail
)


def get_attributes_values_combined(df, attribute):
    for row in df[df['Attributes'] == attribute]['Values']:
        for value in row.split(','):
            yield value.strip()


def get_attributes_values_by_category(df, attribute, category):
    for row in df[(df['Attributes'] == attribute) & (df['Category'] == category)]['Values']:
        for value in row.split(','):
            yield value.strip()


class Command(BaseCommand):
    help = 'Populate Taxonomy Models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            help='The s3 file to read data from',
            required=True
        )

    @staticmethod
    def _populate(model, values):
        # model.objects.bulk_create([model(name=value) for value in values])
        for value in values:
            obj, created = model.objects.get_or_create(name=value)
            if created:
                obj.save()

    @transaction.atomic
    def handle(self, *args, **options):
        filename = options['file']
        df = pd.read_csv(f's3://rossi-rei-data/manufacturers/data/{filename}')
        categories = df['Category'].unique().tolist()
        self._populate(Category, categories)
        colors = set(get_attributes_values_combined(df, 'Color'))
        self._populate(Color, colors)
        for attribute, model in (
                ('Design Details', DesignDetail),
                ('Material', Material),
                ('Type', Type)):
            values = set(get_attributes_values_combined(df, attribute))
            self._populate(model, values)
        for category in categories:
            for attribute, base_model, model, argname in (
                    ('Design Details', DesignDetail, CategoryDesignDetail, 'design_detail'),
                    ('Material', Material, CategoryMaterial, 'material'),
                    ('Type', Type, CategoryType, 'type')):
                values = set(get_attributes_values_by_category(df, attribute, category))
                c_obj = Category.objects.get(name=category)
                for v in values:
                    v_obj = base_model.objects.get(name=v)
                    m_obj = model(**{'category': c_obj, argname: v_obj})
                    try:
                        m_obj.save()
                    except ValidationError:
                        pass
