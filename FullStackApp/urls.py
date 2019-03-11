from django.urls import path


from FullStackApp.views import Home, ProductDetail, Cart, Checkout, ListProductCategory

app_name = 'FullStackApp'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('product/categories/', ListProductCategory.as_view(), name='product-category'),
    path('product/<int:pk>/detail/', ProductDetail.as_view(), name='product-detail'),
    path('product/carts/', Cart.as_view(), name='carts'),
    path('product/checkout/', Checkout.as_view(), name='checkout'),

]
