from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.forms import ModelForm

class CreateCustomer(ModelForm):
    pass

class UpdateCustomer(ModelForm):
    pass

class LoginCustomer(View):
    pass

class LogoutCustomer(View):
    pass