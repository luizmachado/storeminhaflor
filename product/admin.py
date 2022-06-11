from django.contrib import admin
from . import models


class VariationInline(admin.TabularInline):
    model = models.Variation
    extra: 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_description',
                    'get_formated_price', 'get_formated_promo_price']
    inlines = [
        VariationInline
    ]


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Variation)
