from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView

from FullStackApp.cart import Cart
from FullStackApp.cart_order import CartOrder
from FullStackApp.forms import CartAddProductForm, CustomerOrderForm
from FullStackApp.models import Product, ShoppingCart, Category, ProductCategory, User, Customer, Orders, OrderDetail


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

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        product_form = CartAddProductForm()
        context_data['product_form'] = product_form
        return context_data


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


class CartOrderSuccess(TemplateView):
    template_name = 'FullStackApp/cart_success.html'


class Checkout(FormView):
    template_name = 'FullStackApp/checkout.html'
    form_class = CustomerOrderForm
    cart_shipping_fee = 0
    total_cart_plus_shipping = 0
    success_url = reverse_lazy('FullStackApp:cart_order_success')

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

    @transaction.atomic
    def form_valid(self, form):
        cart = Cart(self.request)
        if 'cart_shipping_fee' in self.request.session:
            self.cart_shipping_fee = Decimal(self.request.session['cart_shipping_fee'])

        if cart.get_total_price():
            self.total_cart_plus_shipping = cart.get_total_price() + self.cart_shipping_fee

        if not cart:
            return redirect('FullStackApp:carts')
        print(form.cleaned_data)
        create_account = form.cleaned_data['create_account']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        company = form.cleaned_data['company']
        shipping_region = country = form.cleaned_data['country']
        address = form.cleaned_data['address']
        address_2 = form.cleaned_data['address_2']
        zipcode = form.cleaned_data['zipcode']
        city = form.cleaned_data['city']
        phone_number = form.cleaned_data['phone_number']
        username = email = form.cleaned_data['email']

        NEXT_DAY = 'Nxt_day'
        STANDARD = 'std'
        FREE = 'Free'
        shipping_type = FREE
        if not self.cart_shipping_fee:
            self.cart_shipping_fee =0
        if 0 < self.cart_shipping_fee < 2:
            shipping_type = STANDARD
        elif self.cart_shipping_fee >= 2:
            shipping_type = NEXT_DAY
        order_cart = CartOrder()
        order = order_cart.create_order(total_amount=self.total_cart_plus_shipping,
                                    shipping_type=shipping_type,
                                    shipping_fee=self.cart_shipping_fee,
                                    shipping_region=shipping_region)

        print('order', order)
        cart_list = []
        for item in cart:
            product = item['product']
            size = product.get_default_size()
            color = product.get_default_colour()
            attributes = 'size: {}\n'.format(self)
            attributes += 'color: {}'.format(color)
            cart_list.append({
                'order':order,
                'product':product,
                'attributes': attributes,
                'product_name':product.name,
                'unit_cost':item['price'],
                'quantity':item['quantity'],
            })
        print('car_list', cart_list)
        order_detail = OrderDetail.objects.bulk_create(
            [OrderDetail(**q) for q in cart_list]
        )

        print('order detail', order_detail)
        # //send email to customer on order
        print(create_account)
        if create_account:
            password = User.objects.make_random_password()
            # hash_password = make_password(password)
            user = User(first_name=first_name, last_name=last_name,
                        email=email, username=email, phone_number=phone_number,
                        is_customer=True)
            user.set_password(password)
            user.save()
            print('user', user)
            # //send email to customer
            customer = Customer.objects.create(user=user, company=company,
                                address_1=address, address_2=address_2,
                                city=city, region='Europe',
                                postal_code=zipcode, country='America',
                                shipping_region=shipping_region,
                                day_phone=phone_number)
            order.customer = customer
            print('customer', customer)
            order.save()
        cart.clear()
        response = super().form_valid(form)

        return response


