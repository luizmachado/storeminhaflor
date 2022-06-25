from django.template import Library
from utils import accounting



register = Library()


# Format price to Brazilian Real currency
@register.filter
def format_price_brl(value):
    return f'R$ {value:.2f}'.replace('.', ',')

@register.filter
def cart_total_qtd(cart):
    return accounting.cart_total_quantity(cart)