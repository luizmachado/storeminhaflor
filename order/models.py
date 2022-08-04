from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    total = models.FloatField(verbose_name='Total')
    qtd_total = models.PositiveIntegerField(verbose_name='Qtd Total')
    status = models.CharField(
        verbose_name='Status',
        default="C",
        max_length=1,
        choices=(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        ),
    )

    def __str__(self) -> str:
        return f'Pedido nº {self.pk}'

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name='Pedido')
    product = models.CharField(max_length=255, verbose_name='Produto')
    product_id = models.PositiveIntegerField(verbose_name='ID Produto')
    variation = models.CharField(
        max_length=255, verbose_name='Variação produto')
    variation_id = models.PositiveIntegerField(
        verbose_name='ID Variação produto')
    price = models.FloatField(verbose_name='Preço')
    # TODO: Verify the need of this property
    promotional_price = models.FloatField(
        default=0, verbose_name='Valor promocional')
    quantity = models.PositiveIntegerField(verbose_name='Quantidade')
    image = models.CharField(max_length=2000)


def __str__(self):
    return f'Item do {self.pedido}'


class Meta:
    verbose_name = 'Item do pedido'
    verbose_name_plural = 'Itens do pedido'
