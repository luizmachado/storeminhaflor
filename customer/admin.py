from django.contrib import admin
from . import models

class CustomerAddressInline(admin.StackedInline):
    model = models.CustomerAddress
    extra = 1

class CustomerAdmin(admin.ModelAdmin):
    inlines = [
        CustomerAddressInline
    ]


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.CustomerAddress)