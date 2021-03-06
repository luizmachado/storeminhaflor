# Generated by Django 3.2.13 on 2022-06-09 01:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField(verbose_name='Total')),
                ('status', models.CharField(choices=[('A', 'Aprovado'), ('C', 'Criado'), ('R', 'Reprovado'), ('P', 'Pendente'), ('E', 'Enviado'), ('F', 'Finalizado')], default='C', max_length=1, verbose_name='Status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=255, verbose_name='Produto')),
                ('product_id', models.PositiveIntegerField(verbose_name='ID Produto')),
                ('variation', models.CharField(max_length=255, verbose_name='Variação produto')),
                ('variation_id', models.PositiveIntegerField(verbose_name='ID Variação produto')),
                ('price', models.FloatField(verbose_name='Preço')),
                ('price_discount', models.FloatField(default=0, verbose_name='Valor promocional')),
                ('image', models.CharField(max_length=2000)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order', verbose_name='Pedido')),
            ],
        ),
    ]
