from .cart import Cart

def create_session(request):
    cart_session = Cart(request)
    return({'cart_quantity':cart_session.show_quantity()})


