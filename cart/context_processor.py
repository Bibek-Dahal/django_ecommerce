from .cart import Cart

def create_session(request):
    return({'cart_session':Cart(request)})


