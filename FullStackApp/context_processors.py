from FullStackApp.cart import Cart


def cart(request):
    # Create fixed data structures to pass to template
    # data could equally come from database queries
    # web services or social APIs
    cart_object = Cart(request)
    cart_items = {'items_number': len(cart_object), 'total_price': cart_object.get_total_price()}
    return {'carts_processor': cart_items}

