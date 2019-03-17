from django.core.serializers import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from FullStackApp.forms import CartAddProductForm, CartUpdateProductForm
from FullStackApp.models import Product
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
        return redirect('FullStackApp:carts')
    return redirect('FullStackApp:home')


# def cart_single_update(request):
#     data = request.POST
#     print(data)
#     data = dict(data.lists())
#     # print(data)
#     cart = Cart(request)
#     product_ids = list(data['product_ids[]'])
#
#
#     error = False
#     response = {}
#     print(product_ids)
#     for product_id in product_ids:
#         product = get_object_or_404(Product, id=product_id)
#         quantity = int(data['quantity[{}]'.format(product_id)][0])
#         print("product_id:{} and quantity:{}".format(product_id,quantity))
#         cart.add(product=product, quantity=quantity, update_quantity=True)
#
#     response['error'] = error
#     response['msg'] = 'Cart Successfully updated'
#     return JsonResponse(response)

@require_POST
def cart_update(request):
    data = request.POST
    print(data)
    data = dict(data.lists())
    # print(data)
    cart = Cart(request)
    product_ids = list(data['product_ids[]'])


    error = False
    response = {}
    print(product_ids)
    for product_id in product_ids:
        product = get_object_or_404(Product, id=product_id)
        quantity = int(data['quantity[{}]'.format(product_id)][0])
        print("product_id:{} and quantity:{}".format(product_id, quantity))
        cart.add(product=product, quantity=quantity, update_quantity=True)

    response['error'] = error
    response['msg'] = 'Cart Successfully updated'
    return JsonResponse(response)


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('FullStackApp:carts')

def cart_remove_all(request):
    cart = Cart(request)
    # cart.remove_all()
    cart.clear()
    return redirect('FullStackApp:carts')

def cart_lists(request):
    cart = Cart(request)
    print(len(cart))
    for item in cart:
        print(item)
        item['update_quantity_form'] = CartUpdateProductForm(initial={'quantity': item['quantity'], 'update': True})
    print('final cart', cart)

    return render(request, 'FullStackApp/cart.html', {'carts': cart})

@require_POST
def cart_pre_checkout(request):
    data = request.POST
    print(data)
    cart_shipping_fee = data['cart_shipping_fee']
    print(cart_shipping_fee)
    request.session['cart_shipping_fee'] = cart_shipping_fee
    return redirect('FullStackApp:checkout')

