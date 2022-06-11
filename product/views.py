from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse


class ListProducts(ListView):
    def get(self, *args, **kwargs):
        return HttpResponse('ListProducts')

class DetailProducts(View):
    def get(self, *args, **kwargs):
        return HttpResponse('DetailProducts')

class AddCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('AddCart')

class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoveFromCart')

class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Cart')

class Checkout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Checkout')
