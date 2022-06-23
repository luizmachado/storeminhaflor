from django.template import Library



register = Library()


# Format price to Brazilian Real currency
@register.filter
def format_price_brl(value):
    return f'R$ {value:.2f}'.replace('.', ',')