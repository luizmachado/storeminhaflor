# Generated by Django 3.2.13 on 2022-06-09 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20220608_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='stock',
            field=models.PositiveIntegerField(default=1, verbose_name='Estoque'),
        ),
    ]
