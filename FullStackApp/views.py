from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView

from FullStackApp.cart import Cart
from FullStackApp.forms import CartAddProductForm, CustomerOrderForm
from FullStackApp.models import Product, ShoppingCart, Category, ProductCategory


class ListProduct(ListView):
    template_name = 'FullStackApp/index.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()
        product_form = CartAddProductForm()
        context_data['product_form'] = product_form
        return context_data


class ListProductCategory(ListProduct):
    template_name = 'FullStackApp/categories.html'
    current_category = 'All'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'categories' in self.request.GET:
            categories = self.request.GET.get('categories')
            print(categories)
            category = Category.objects.filter(name=categories)
            # product_category_id = ProductCategory.objects.filter(category=category)
            # Product.objects.filter(related_product__category=)
            if category:
                category = category[0]
                qs = qs.filter(related_product__category=category)
                self.current_category = categories
                self.paginate_by = None
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()
        context_data['categories'] = Category.objects.all()
        context_data['current_category'] = self.current_category

        return context_data


class ProductDetail(DetailView):
    template_name = 'FullStackApp/product.html'
    model = Product
    context_object_name = 'product'


class Home(View):
    def get(self, request, *args, **kwargs):
        view = ListProduct.as_view()
        return view(request, *args, **kwargs)


class ListCart(ListView):
    template_name = 'FullStackApp/cart.html'
    model = ShoppingCart
    context_object_name = 'carts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(buy_now=True)
        return qs


# @method_decorator([login_required, ], name='dispatch')
class CartViewList(View):
    def get(self, request, *args, **kwargs):
        view = ListCart.as_view()
        return view(request, *args, **kwargs)

    pass


class Checkout(FormView):
    template_name = 'FullStackApp/checkout.html'
    form_class = CustomerOrderForm
    cart_shipping_fee = 0
    total_cart_plus_shipping = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'cart_shipping_fee' in self.request.session:
            self.cart_shipping_fee = Decimal(self.request.session['cart_shipping_fee'])
        cart = Cart(self.request)
        if cart.get_total_price():
            self.total_cart_plus_shipping = cart.get_total_price() + self.cart_shipping_fee

        context['total_cart_plus_shipping'] = self.total_cart_plus_shipping
        context['cart_shipping_fee'] = self.cart_shipping_fee
        return context


    def form_valid(self, form):
        print(form.cleaned_data)
        create_account = form.cleaned_data['create_account']
        print(create_account)
