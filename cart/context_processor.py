from .cart import Cart

def create_session(request):
    cart_quantity = Cart(request)
    return({'cart_quantity':cart_quantity.show_quantity()})


