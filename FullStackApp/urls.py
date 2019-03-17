from django.urls import path

from FullStackApp.cart_views import cart_add, cart_remove, cart_update, cart_lists, cart_remove_all, cart_pre_checkout
from FullStackApp.views import Home, ProductDetail, CartViewList, Checkout, ListProductCategory

app_name = 'FullStackApp'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('product/categories/', ListProductCategory.as_view(), name='product-category'),
    path('product/<int:pk>/detail/', ProductDetail.as_view(), name='product-detail'),
    path('product/carts/', cart_lists, name='carts'),
    path('product/checkout/', Checkout.as_view(), name='checkout'),
    path('product/pre-checkout/', cart_pre_checkout, name='pre-checkout'),
    path('product/<int:product_id>/carts/add/', cart_add, name='product-add'),
    path('product/<int:product_id>/carts/remove/', cart_remove, name='product-remove'),
    path('product/carts/clear/', cart_remove_all, name='product-remove-all'),
    path('product/carts/update/', cart_update, name='product-update'),

]
