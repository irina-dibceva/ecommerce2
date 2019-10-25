from django.urls import path

from .views import home, cart_update

urlpatterns = [
    path('', home),
    path('update/', cart_update),
]
