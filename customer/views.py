from curses.ascii import HT
from urllib import request
from webbrowser import get
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.list import ListView
from django.views import View
from django.forms import ModelForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
import copy
from . import models
from . import forms

# Parent class to Create and Update Customer


class BaseCustomer(View):
    template_name = 'customer/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        self.profile = None

        if self.request.user.is_authenticated:
            self.profile = models.Customer.objects.filter(
                user=self.request.user).first()
            self.address = models.CustomerAddress.objects.filter(
                user=self.profile).first()

            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user,
                ),
                'customerform': forms.CustomerForm(
                    data=self.request.POST or None,
                    instance=self.profile
                ),
                'customeraddressform': forms.CustomerAddressForm(
                    data=self.request.POST or None,
                    instance=self.address
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

        if self.request.user.is_authenticated:
            self.template_name = 'customer/update.html'

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

        # Logged user (update)
        if self.request.user.is_authenticated:
            user_customer = get_object_or_404(
                User, username=self.request.user.username)

            user_customer.username = username

            if password:
                user_customer.set_password(password)
            user_customer.email = email
            user_customer.first_name = first_name
            user_customer.last_name = last_name
            user_customer.save()

            if not self.profile:
                self.customerform.cleaned_data['user'] = user_customer
                profile = models.Customer(**self.customerform.cleaned_data)
                profile.save()
            else:
                profile = self.customerform.save(commit=False)
                profile.user = user_customer
                profile.save()
            if not self.address:
                self.customeraddressform.cleaned_data['user'] = profile
                address = models.CustomerAddress(
                    **self.customeraddressform.cleaned_data)
                address.save()
            else:
                address = self.customeraddressform.save(commit=False)
                address.user = profile
                address.save()

        # Unlogged user (create)
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

        if password:
            autentica = authenticate(
                self.request,
                username=user_customer,
                password=password
            )

            if autentica:
                login(self.request, user=user_customer)

        self.request.session['cart'] = self.cart
        self.request.session.save()

        messages.success(
            self.request,
            'Seu cadastro foi criado/atualizado com sucesso !'
        )

        return redirect('customer:create')


class UpdateCustomer(BaseCustomer):
    def get(self, *args, **kwargs):
        return HttpResponse('UpdateCustomer')


class LoginCustomer(View):
    def get(self, *args, **kwargs):
        return HttpResponse('LoginCustomer')


class LogoutCustomer(View):
    def get(self, *args, **kwargs):
        return HttpResponse('LogoutCustomer')
