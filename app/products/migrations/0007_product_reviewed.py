# Generated by Django 3.0.5 on 2020-04-25 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_manufacturer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='reviewed',
            field=models.BooleanField(default=False),
        ),
    ]
