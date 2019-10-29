from django.urls import path

from .views import home, cart_update, checkout_home

urlpatterns = [
    path('', home),
    path('update/', cart_update),
    path('checkout/', checkout_home),
]
