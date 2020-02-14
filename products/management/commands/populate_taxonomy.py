from django.core.management.base import BaseCommand

from products.models import Category, Color, DesignDetail, Material, Type

categories = ('Bags', 'Wallets')

colors = (
    'Black',
    'Blue',
    'Brown',
    'Green',
    'Grey',
    'Multicolor',
    'Neutral',
    'Orange',
    'Pink',
    'Purple',
    'Red',
    'White',
    'Yellow'
)

design_details = (
    'Bow',
    'Buckle',
    'Clasp',
    'Crossbody Strap',
    'Drawstring',
    'Knot',
    'Lock',
    'Metal',
    'Metal Chain',
    'Studs',
    'Top Handle',
    'Woven',
    'Zipper'
)

materials = (
    'Cordura',
    'Cotton Canvas',
    'Croc',
    'Denim',
    'Embossed-croc',
    'Embossed-python',
    'Haircalf',
    'Knit',
    'Leather',
    'Mesh',
    'Metal',
    'Neoprene',
    'Nylon',
    'Plastic',
    'Python',
    'Straw',
    'Vacchetta',
    'Vegan',
    'Vegetable-tanned leather'
)

types = (
    'Backpack',
    'Baguette',
    'Belt',
    'Bifold',
    'Briefcase',
    'Bucket',
    'Camera',
    'Card Case',
    'Clutch',
    'Crossbody',
    'Doctor’s',
    'Duffle',
    'Envelope',
    'Fanny Pack',
    'Garment',
    'Gym',
    'Hobo',
    'ID Card',
    'Laptop',
    'Large',
    'Messenger',
    'Money Clip',
    'Passport Holder',
    'Portfolio',
    'Pouch',
    'Saddle',
    'Satchel',
    'Slingback',
    'Totes',
    'Travel',
    'Trifold',
    'Zippered'
)


class Command(BaseCommand):
    help = 'Populate Taxonomy Models: Category, Color, DesignDetail, Material, Type'

    def add_arguments(self, parser):
        parser.add_argument(
            '--category',
            action='store_true',
            help='Populate Category with default values',
        )
        parser.add_argument(
            '--color',
            action='store_true',
            help='Populate Color with default values',
        )
        parser.add_argument(
            '--design',
            action='store_true',
            help='Populate DesignDetails with default values',
        )
        parser.add_argument(
            '--material',
            action='store_true',
            help='Populate Material with default values',
        )
        parser.add_argument(
            '--type',
            action='store_true',
            help='Populate Type with default values',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Populate all taxonomy Models with default value',
        )

    def _populate(self, model, values):
        model.objects.bulk_create([
            model(name=value) for value in values
        ])

    def handle(self, *args, **options):
        if options['all']:
            for model, values in [
                (Category, categories),
                (Color, colors),
                (DesignDetail, design_details),
                (Material, materials),
                (Type, types)
            ]:
                self._populate(model, values)
        else:
            if options['category']:
                self._populate(Category, categories)
            if options['color']:
                self._populate(Color, colors)
            if options['design']:
                self._populate(DesignDetail, design_details)
            if options['material']:
                self._populate(DesignDetail, design_details)
