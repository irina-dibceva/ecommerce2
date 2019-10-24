from django.urls import path

from .views import ProductDetailView, ProductListView, ProductDetailSlugView, product_list, product_detail, \
    ProductFeatureDetailView, ProductFeatureListView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('featured/', ProductFeatureListView.as_view()),
    path('featured/<str:slug>/', ProductFeatureDetailView.as_view()),
    path('<str:slug>/', ProductDetailSlugView.as_view()),
    path('detail/', product_detail),
    # path('feature/<int:pk>/', ProductFeatureDetailView.as_view()),
    # path('feature/', ProductFeatureListView.as_view()),
]
