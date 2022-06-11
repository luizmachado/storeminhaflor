from curses.ascii import HT
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.forms import ModelForm
from django.http import HttpResponse

class CreateCustomer(View):
    def get(self, *args, **kwargs):
        return HttpResponse('CreateCustomer')

class UpdateCustomer(View):
    def get(self,*args, **kwargs):
        return HttpResponse('UpdateCustomer')

class LoginCustomer(View):
    def get(self,*args, **kwargs):
        return HttpResponse('LoginCustomer')

class LogoutCustomer(View):
    def get(self,*args, **kwargs):
        return HttpResponse('LogoutCustomer')