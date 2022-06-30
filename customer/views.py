from curses.ascii import HT
from urllib import request
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.forms import ModelForm
from django.http import HttpResponse
from . import models
from . import forms

# Parent class to Create and Update Customer


class BaseCustomer(View):
    template_name = 'customer/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        if self.request.user.is_authenticated:
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                'customerform': forms.CustomerForm(
                    data=self.request.POST or None
                ),
                'customeraddressform': forms.CustomerAddressForm(
                    data=self.request.POST or None
                )
            }
        else:
            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None
                ),
                'customerform': forms.CustomerForm(
                    data=self.request.POST or None
                ),
                'customeraddressform': forms.CustomerAddressForm(
                    data=self.request.POST or None
                )
            }
        
        self.userform = self.context['userform']
        self.customerform = self.context['customerform']
        self.customeraddressform = self.context['customeraddressform']

        self.rendering = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.rendering

class CreateCustomer(BaseCustomer):
    def post(self, *args, **kwargs):
        return self.rendering


class UpdateCustomer(BaseCustomer):
    def get(self, *args, **kwargs):
        return HttpResponse('UpdateCustomer')


class LoginCustomer(View):
    def get(self, *args, **kwargs):
        return HttpResponse('LoginCustomer')


class LogoutCustomer(View):
    def get(self, *args, **kwargs):
        return HttpResponse('LogoutCustomer')
