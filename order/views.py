from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views import View
from django.forms import ModelForm
from django.http import HttpResponse
from django.contrib import messages
from customer.models import Customer, CustomerAddress
from product.models import Variation
from . import models

class PayOrder(View):
    template_name = 'order/pay.html'

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
        return render(self.request, self.template_name, context)

class SaveOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('CloseOrder')

class DetailOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('DetailOrder')