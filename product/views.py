from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from pprint import pprint
from . import models


class ListProducts(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 6


class DetailProducts(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwargs = 'slug'


class AddCart(View):
    def get(self, *args, **kwargs):
        #TODO: Remove lines below before deploy, its been used to clean cart
        # if self.request.session.get('cart'):
        #     del self.request.session['cart']
        #     self.request.session.save()
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            messages.error(
                self.request,
                'Produto inválido'
            )
            return redirect(http_referer)

        variation = get_object_or_404(models.Variation, id=variation_id)

        if variation.stock < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)

        product = variation.product
        product_id = product.id
        product_name = product.name
        variation_name = variation.name or ''
        unit_price = variation.price
        unit_promo_price = variation.promotional_price
        slug = product.slug
        image = product.image
        variation_stock = variation.stock

        if image:
            image = image.name
        else:
            image = ''

        # Create a session with cart key if not exist
        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            quantity_cart = cart[variation_id]['quantity']
            quantity_cart += 1

            if variation_stock < quantity_cart:
                messages.error(
                    self.request,
                    f'Estoque insuficiente para {quantity_cart} x do '
                    f'produto "{product_name} {variation_name}". Adicionamos '
                    f'{variation_stock} x no seu carrinho'
                )
                quantity_cart = variation_stock
            else:
                messages.success(
                    self.request,
                    f'Produto {product_name} {variation_name}, adicionados com sucesso'
                )
        
            cart[variation_id]['quantity'] = quantity_cart
            cart[variation_id]['quantity_price'] = unit_price * quantity_cart
            cart[variation_id]['quantity_promo_price'] = unit_promo_price * quantity_cart
        else:
            cart[variation_id] = {
                'product_id' : product_id,
                'variation_id' : variation_id,
                'product_name' : product_name,
                'variation_name' : variation_name,
                'unit_price' : unit_price,
                'unit_promo_price' : unit_promo_price,
                'quantity_price' : unit_price,
                'quantity_promo_price' : unit_promo_price,
                'quantity' : 1,
                'slug' : slug,
                'image' : image
            }

        self.request.session.save()
        return redirect(http_referer)


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            return redirect(http_referer)
        
        if variation_id not in self.request.session['cart']:
            return redirect(http_referer)

        cart = self.request.session['cart'][variation_id]

        messages.success(
            self.request,
            f'Produto {cart["product_name"]} {cart["variation_name"]}'
            f'removido do carrinho'
        )
        del self.request.session['cart'][variation_id]
        self.request.session.save()

        return redirect(http_referer)


class Cart(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'product/cart.html')


class OrderSummary(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Checkout')
