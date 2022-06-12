from django.db import models
from pathlib import Path
from django.conf import settings
from django.utils.text import slugify
from PIL import Image


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome produto')
    short_description = models.TextField(
        max_length=255, verbose_name='Descrição curta')
    long_description = models.TextField(verbose_name='Descrição longa')
    image = models.ImageField(
        upload_to='product_images/%Y/%m/', verbose_name='Imagem', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    mkt_price = models.FloatField(verbose_name='Preço de exibição')
    mkt_price_promotional = models.FloatField(
        default=0, verbose_name='Preço promocional de exibição')
    type_product = models.CharField(
        default='V',
        max_length=1,
        verbose_name='Tipo de produto',
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        ))

    # Format price visualization
    def get_formated_price(self):
        return f'R$ {self.mkt_price:.2f}'.replace('.', ',')

    def get_formated_promo_price(self):
        return f'R$ {self.mkt_price_promotional:.2f}'.replace('.', ',')
        
    # Change Django Admin Product preview description
    get_formated_price.short_description = 'Preço'
    get_formated_promo_price.short_description = 'Preço promocional'

    def __str__(self) -> str:
        return self.name

    class Meta():
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def save(self, *args, **kwargs):
        # Generate slug automatically
        if not self.slug:
            slug = f'{slugify(self.name)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_image_size = 800

        # Function to automatically resize product images
        if self.image:
            self.resize_image(self.image.name, max_image_size)

    # Method to resize images
    @staticmethod
    def resize_image(image_name, new_width):
        image_path = Path(settings.MEDIA_ROOT / image_name)
        img = Image.open(image_path)
        width, height = img.size
        if width <= 800:
            img.close()
            return
        new_height = round((height * new_width) / width)
        new_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        new_img.save(
            image_path,
            optimize=True,
            quality=60,
        )
        img.close()
        new_img.close()

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Modelo')
    name = models.CharField(max_length=50, verbose_name='Nome', blank=True, null=True)
    price = models.FloatField(verbose_name='Preço')
    promotional_price = models.FloatField(default=0, verbose_name='Preço promocional')
    stock = models.PositiveIntegerField(default=1, verbose_name='Estoque')

    def __str__(self) -> str:
        return self.name or self.product.name

    def Meta():
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'