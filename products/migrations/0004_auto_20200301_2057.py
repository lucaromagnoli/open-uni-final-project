# Generated by Django 3.0.3 on 2020-03-01 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_product_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_url',
            field=models.URLField(unique=True),
        ),
    ]
