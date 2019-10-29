from .models import Cart


def cart_count(request):
    data = {'cart_count': 0}
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            data['cart_count'] = cart.products.count()
    return data
