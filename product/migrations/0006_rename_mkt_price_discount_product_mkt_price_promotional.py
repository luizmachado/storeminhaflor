# Generated by Django 3.2.13 on 2022-06-11 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_product_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='mkt_price_discount',
            new_name='mkt_price_promotional',
        ),
    ]
