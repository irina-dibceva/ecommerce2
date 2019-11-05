from django.urls import path

from .views import home, cart_update, checkout_home, checkout_done_view

app_name = 'cart'

urlpatterns = [
    path('', home, name='cart-home'),
    path('update/', cart_update, name='update'),
    path('checkout/', checkout_home, name='checkout'),
    path('checkout/success/', checkout_done_view, name='success'),
]
