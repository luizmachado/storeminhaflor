from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.forms import ModelForm
from django.http import HttpResponse

class PayOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('PayOrder')

class CloseOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('CloseOrder')

class DetailOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('DetailOrder')