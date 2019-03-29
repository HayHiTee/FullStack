from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView
from paypal.standard.forms import PayPalPaymentsForm

from FullStack.settings import PAYPAL_RECEIVER_EMAIL
from FullStackApp.cart import Cart
from FullStackApp.cart_order import CartOrder
from FullStackApp.decorators import customer_required
from FullStackApp.email import send_email_account_created, send_order_email
from FullStackApp.forms import CartAddProductForm, CustomerOrderForm, CustomerRegistrationForm
from FullStackApp.models import Product, ShoppingCart, Category, ProductCategory, User, Customer, Orders, OrderDetail, \
    Shipping


# Class that lists all the orders requested by the customer to the customer
@method_decorator([login_required, customer_required], name='dispatch')
class ListOrders(ListView):
    template_name = 'FullStackApp/orders.html'
    model = Orders
    context_object_name = 'orders'
    paginate_by = 10
    pass

    def get_queryset(self):
        qs = super().get_queryset()
        customer = Customer.objects.get(user = self.request.user)
        qs = qs.filter(customer=customer)
        return qs


# Class that lists all the orders details requested by the customer to the customer
@method_decorator([login_required, customer_required], name='dispatch')
class OrderDetailView(DetailView):
    template_name = 'FullStackApp/order_details.html'
    model = Orders
    context_object_name = 'order_detail'

    def get_queryset(self):
        qs = super().get_queryset()
        customer = Customer.objects.get(user=self.request.user)
        qs = qs.filter(customer=customer)
        return qs
    pass


# class ListOrderDetails(ListView):
#     template_name = 'FullStackApp/order_details.html'
#     model = OrderDetail
#     context_object_name = 'order_details'


# Class that lists all the Product available in the database
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


# Class that lists all the Product Category available in the database
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


# Class that shows each Product details available in the database
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

# Order SUccess page Class
class CartOrderSuccess(TemplateView):
    template_name = 'FullStackApp/cart_success.html'


class CustomerRegistrationView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        username = form.cleaned_data['username']
        send_email_account_created(email, username, password, self.request)
        response = super().form_valid(form)
        return response


# Checkout View Class
class Checkout(FormView):
    template_name = 'FullStackApp/checkout.html'
    form_class = CustomerOrderForm
    cart_shipping_fee = 0
    total_cart_plus_shipping = 0
    success_url = reverse_lazy('FullStackApp:cart_order_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # shipping = None
        if 'cart_shipping_id' in self.request.session:
            shipping_id = self.request.session['cart_shipping_id']
            shipping = Shipping.objects.get(id=shipping_id)
            self.cart_shipping_fee = Decimal(shipping.shipping_cost)

        cart = Cart(self.request)
        if cart.get_total_price():
            self.total_cart_plus_shipping = cart.get_total_price() + self.cart_shipping_fee

        
        context['total_cart_plus_shipping'] = self.total_cart_plus_shipping
        context['cart_shipping_fee'] = self.cart_shipping_fee
        return context

    @transaction.atomic
    def form_valid(self, form):
        cart = Cart(self.request)
        shipping = None
        if 'cart_shipping_id' in self.request.session:
            shipping_id = self.request.session['cart_shipping_id']
            shipping = Shipping.objects.get(id=shipping_id)
            self.cart_shipping_fee = Decimal(shipping.shipping_cost)

        if cart.get_total_price():
            self.total_cart_plus_shipping = cart.get_total_price() + self.cart_shipping_fee

        if not cart or not shipping:
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
        order_cart = CartOrder()
        order = order_cart.create_order(total_amount=self.total_cart_plus_shipping, shipping=shipping)

        print('order', order)
        cart_list = []
        for item in cart:
            product = item['product']
            size = product.get_default_size()
            color = product.get_default_colour()
            attributes = 'size: {}\n'.format(size)
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
        send_order_email(email, order.tracking_id, self.request)
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
            send_email_account_created(email, email, password, self.request)
            order.save()
        cart.clear()
        response = super().form_valid(form)

        return response


# CHeck out for alaready registered and Valid AUTH CUSTOMER
@require_POST
@transaction.atomic
def check_out_auth_customer(request):
    template_name = 'FullStackApp/checkout.html'
    cart_shipping_fee = 0
    total_cart_plus_shipping = 0
    success_url = reverse_lazy('FullStackApp:cart_order_success')
    context = {}
    shipping = None
    if 'cart_shipping_id' in request.session:
        shipping_id = request.session['cart_shipping_id']
        shipping = Shipping.objects.get(id=shipping_id)
        cart_shipping_fee = Decimal(shipping.shipping_cost)

    cart = Cart(request)
    if cart.get_total_price():
        total_cart_plus_shipping = cart.get_total_price() + cart_shipping_fee
    if not cart or not shipping:
        return redirect('FullStackApp:carts')
    context['total_cart_plus_shipping'] = total_cart_plus_shipping
    context['cart_shipping_fee'] = cart_shipping_fee

    customer = Customer.objects.get(user=request.user)
    order_cart = CartOrder()
    order = order_cart.create_order(total_amount=total_cart_plus_shipping, shipping=shipping)
    order.customer = customer
    order.save()
    print('order', order)
    cart_list = []
    for item in cart:
        product = item['product']
        size = product.get_default_size()
        color = product.get_default_colour()
        attributes = 'size: {}\n'.format(size)
        attributes += 'color: {}'.format(color)
        cart_list.append({
            'order': order,
            'product': product,
            'attributes': attributes,
            'product_name': product.name,
            'unit_cost': item['price'],
            'quantity': item['quantity'],
        })
    print('car_list', cart_list)
    order_detail = OrderDetail.objects.bulk_create(
        [OrderDetail(**q) for q in cart_list]
    )

    return redirect('FullStackApp:cart_order_success')


def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        "business": PAYPAL_RECEIVER_EMAIL,
        "amount": 1000.00,
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('FullStackApp:cart_order_success')),
        "cancel_return": request.build_absolute_uri(reverse('FullStackApp:carts')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    print(paypal_dict)
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "FullStackApp/payment.html", context)


# def paypal_return_view(request):
#     pass