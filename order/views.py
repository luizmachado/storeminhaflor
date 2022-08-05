from multiprocessing import context
from telnetlib import STATUS
from django.shortcuts import render, redirect, reverse
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views import View
from django.forms import ModelForm
from django.http import HttpResponse
from django.contrib import messages
from customer.models import Customer, CustomerAddress
from product.models import Variation
from utils import accounting
from . import models


class DispatchLoginRequired(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('customer:create')

        return super().dispatch(*args, **kwargs)

class SaveOrder(View):
    template_name = 'order/saveorder.html'

    def get(self, *args, **kwargs):
        # Check if user is logged
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa efetuar o login.'
            )
            return redirect('customer:create')

        # Check if there is any product in the cart
        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Seu carrinho de compras está vazio, aproveite as promoções !'
            )
            return redirect('product:list')

        # Check if customer there is a profile and address
        profile = Customer.objects.filter(
            user=self.request.user).exists()
        address = CustomerAddress.objects.filter(
            user=profile).exists()

        # Check if customer there is profile and address
        if not profile or address:
            messages.error(
                self.request,
                'Usuário sem perfil ou endereço'
            )
            return redirect('customer:create')

        cart = self.request.session.get('cart')
        cart_variation_ids = [v for v in cart]
        bd_variations = list(Variation.objects.select_related('product')
                             .filter(id__in=cart_variation_ids))

        msg_error = []
        for variation in bd_variations:
            vid = str(variation.id)
            vstock = variation.stock
            vqty = cart[vid]['quantity']
            vuniprice = cart[vid]['unit_price']
            vunipromoprice = cart[vid]['unit_promo_price']

            if vstock < vqty:
                cart[vid]['quantity'] = vstock
                cart[vid]['quantity_price'] = vstock * vuniprice
                cart[vid]['quantity_promo_price'] = vstock * vunipromoprice
                self.request.session.save()

                msg_error.append(f'Não há estoque suficiente do produto '
                                 f'{cart[vid]["product_name"]}! A quantidade foi reduzida,'
                                 f'verifique seu carrinho !')

        if msg_error:
            for indice, msg in enumerate(msg_error):
                messages.error(
                    self.request,
                    msg_error[indice]
                )
            return redirect('product:cart')

        qtd_total_cart = accounting.cart_total_quantity(cart)
        price_total_cart = accounting.cart_totals(cart)

        order = models.Order(
            user=self.request.user,
            total=price_total_cart,
            qtd_total=qtd_total_cart,
            status='C',
        )
        order.save()

        models.OrderItem.objects.bulk_create(
            [
                models.OrderItem(
                    order=order,
                    product=v['product_name'],
                    product_id=v['product_id'],
                    variation=v['variation_name'],
                    variation_id=v['variation_id'],
                    price=v['quantity_price'],
                    promotional_price=v['quantity_promo_price'],
                    quantity=v['quantity'],
                    image=v['image'],

                ) for v in cart.values()
            ]
        )

        # Clean cart after save order
        del self.request.session['cart']

        return redirect(
            reverse(
                'order:pay',
                kwargs={
                    'pk': order.pk
                }
            )
        )


class PayOrder(DispatchLoginRequired, DetailView):
    template_name = 'order/pay.html'
    model = models.Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs


class DetailOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('DetailOrder')


class ListOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('ListOrder')
