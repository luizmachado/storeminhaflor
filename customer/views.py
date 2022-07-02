from curses.ascii import HT
from urllib import request
from webbrowser import get
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views import View
from django.forms import ModelForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from . import models
from . import forms

# Parent class to Create and Update Customer


class BaseCustomer(View):
    template_name = 'customer/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.profile = None

        if self.request.user.is_authenticated:
            self.profile = models.Customer.objects.filter(
                user=self.request.user).first()

            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user,
                ),
                'customerform': forms.CustomerForm(
                    data=self.request.POST or None,
                ),
                'customeraddressform': forms.CustomerAddressForm(
                    data=self.request.POST or None,
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
        if not self.userform.is_valid() or not self.customerform.is_valid() \
            or not self.customeraddressform.is_valid():
            return self.rendering

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        #TODO: Load Customer and CustomerAddress information fields if exist
        #Logged user (update)
        if self.request.user.is_authenticated:
            user_customer = get_object_or_404( 
                User, username=self.request.user.username)

            user_customer.username = username

            if password:
                user_customer.set_password(password)
            user_customer.email = email
            user_customer.first_name = first_name
            user_customer.last_name = last_name

            customer = self.customerform.save(commit=False)
            customer.user = user_customer

            customeraddr = self.customeraddressform.save(commit=False)
            customeraddr.user = customer

            user_customer.save()
            customer.save()
            customeraddr.save()

        #Unlogged user (create)
        else:
            user_customer = self.userform.save(commit=False)
            user_customer.set_password(password)
            user_customer.save()
            user_customer.email = email
            user_customer.first_name = first_name
            user_customer.last_name = last_name

            customer = self.customerform.save(commit=False)
            customer.user = user_customer

            customeraddr = self.customeraddressform.save(commit=False)
            customeraddr.user = customer

            user_customer.save()
            customer.save()
            customeraddr.save()



        print('Valido')
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
