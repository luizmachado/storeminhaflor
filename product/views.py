from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View


class ListProducts(ListView):
    pass

class DetailProducts(View):
    pass

class AddCart(View):
    pass

class RemoveFromCart(View):
    pass

class Cart(View):
    pass

class Checkout(View):
    pass
