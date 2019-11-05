import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile
from carts.models import Cart
from orders.models import Order
from products.models import Product

STRIPE_SECRET_KEY = getattr(settings, 'STRIPE_SECRET_KEY', 'sk_test_ptzZQv5hfPxqPYSoskcfic6M00nysZ1CX9')

STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY', 'pk_test_1tqX3Cdgc5sHFCN0Pe2NxNqX00DgsSZ3Fl')
stripe.api_key = STRIPE_SECRET_KEY


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        "id": x.id,
        "url": x.get_absolute_url(),
        "name": x.name,
        "price": x.price
    }
        for x in cart_obj.products.all()]
    cart_data = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)


def home(request):
    cart_obj, is_created = Cart.objects.new(request.user)
    return render(request, 'carts/home.html', {'cart': cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')

    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print('Show message to user, product is gone?')
            return redirect('/cart/')
        cart_obj, new_obj = Cart.objects.new(request.user)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj)
            added = True
        request.session['cart_items'] = cart_obj.products.count()
        # request.session['cart_id'] = cart_obj.id
        if request.is_ajax():  # Asynchronous JavaScript And XML / JSON
            print("Ajax request")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(json_data, status=200)

    return redirect('/cart/')


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None

    if cart_obj.products.count() == 0:
        return redirect('/cart/')

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_card = billing_profile.has_card
    if request.method == "POST":
        "check that order is done"
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    '''
                    is this the best spot?
                    '''
                    billing_profile.set_cards_inactive()
                return redirect("cart:success")
            else:
                print(crg_msg)
                return redirect("cart:checkout")
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY
    }
    return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})
