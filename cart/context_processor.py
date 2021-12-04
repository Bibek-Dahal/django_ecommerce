from .cart import Cart

def cart_quantity(request):
    return({'cart': Cart(request)})


