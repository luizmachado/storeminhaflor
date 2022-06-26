def cart_total_quantity(cart):
    return sum([item['quantity'] for item in cart.values()])

def cart_totals(cart):
    return sum(
        [
        item.get('quantity_promo_price')
        if item.get('quantity_promo_price')
        else item.get('quantity_price')
        for item in cart.values()
        ]
    )