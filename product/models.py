from django.db import models
from pathlib import Path
from django.conf import settings
from PIL import Image


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome produto')
    short_description = models.TextField(
        max_length=255, verbose_name='Descrição curta')
    long_description = models.TextField(verbose_name='Descrição longa')
    image = models.ImageField(
        upload_to='product_images/%Y/%m/', verbose_name='Imagem', blank=True, null=True)
    slug = models.SlugField(unique=True)
    mkt_price = models.FloatField(verbose_name='Preço de exibição')
    mkt_price_discount = models.FloatField(
        default=0, verbose_name='Preço promocional de exibição')
    type_product = models.CharField(
        default='V',
        max_length=1,
        verbose_name='Tipo de produto',
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        ))
    
    def __str__(self) -> str:
        return self.name

    class Meta():
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    # Function to automatically resize product images
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        max_image_size = 800

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

    
