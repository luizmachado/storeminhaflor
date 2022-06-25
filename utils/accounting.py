def cart_total_quantity(cart):
    return sum([item['quantity'] for item in cart.values()])