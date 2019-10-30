from django.urls import path

from .views import home, cart_update, checkout_home, checkout_done_view

urlpatterns = [
    path('', home),
    path('update/', cart_update),
    path('checkout/', checkout_home),
    path('checkout/success/', checkout_done_view),
]
