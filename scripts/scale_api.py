import os

import dotenv
import requests

dotenv.load_dotenv()

category_design_details = None
category_types = None
category_materials = None
colors = None

def create_categorization_task(batch, picture_url, product_metadata, product_category):
        payload = dict(
            batch=batch,
            callback_url=os.environ['CALLBACK_URL'],
            instruction=f'Categorize this {picture_url}',
            attachment_type='image',
            attachment=picture_url,
            taxonomies=create_taxonomies(product_category)
        )


def create_taxonomies(product_category):
    return {
        'design_details': {
            'type': 'category',
            'description': f'Which design detail does the {product_category} have?',
            'choices': category_design_details,
            'allow_multiple': True
        },
        'type': {
            'type': 'category',
            'description': f'Which type of {product_category} is this?',
            'choices': category_types
        },
        'material': {
            'type': 'category',
            'description': f'Which material is the {product_category} made of?',
            'allow_multiple': True,
            'choices': category_materials
        },
        'color': {
            'type': 'category',
            'description': f'Which color is the {product_category}?',
            'choices': colors
        },
    }
