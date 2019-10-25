from django.shortcuts import render, redirect

from carts.models import Cart
from products.models import Product


def home(request):
    # del request.session['cart_id']
    # cart_id = request.session.get('cart_id', None)
    # if cart_id is None:
    #     cart_obj = Cart.objects.create(user=None)
    #     request.session['cart_id'] = cart_obj.id
    # else:
    #     print('Cart id exists')
    #     print(cart_id)
    #     cart_obj = Cart.objects.get(id=cart_id)
    # return render(request, 'carts/home.html', {})
    cart_obj, is_created = Cart.objects.new(request.user)
    # print(cart_obj.id)
    # products = cart_obj.products.all()
    # total = 0
    # for x in products:
    #     total += x.price
    # cart_obj.total = total
    # cart_obj.save()
    return render(request, 'carts/home.html', {'cart': cart_obj})


def cart_update(request):
    print(request.POST)
    product_id = request.POST.get('product')
    print(product_id)
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print('Show message to user, product is gone?')
            return redirect('/cart/')
        cart_obj, new_obj = Cart.objects.new(request.user)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()

    return redirect('/cart/')
