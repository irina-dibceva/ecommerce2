from django.urls import path

from .views import ProductDetailView, ProductListView, ProductDetailSlugView
urlpatterns = [
    path('', ProductListView.as_view()),

    ]
