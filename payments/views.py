import stripe
from django.shortcuts import render, redirect

# Create your views here.


# payments/views.py
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView

from FullStack import settings
from FullStackApp.cart import Cart
from FullStackApp.email import send_order_email
from FullStackApp.models import Orders

stripe.api_key = settings.STRIPE_SECRET_KEY # new


class HomePageView(TemplateView):
    template_name = 'payments/home.html'

    def get(self, request, *args, **kwargs):
        if 'cart_order_id' not in self.request.session:
           return redirect('FullStackApp:carts')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):  # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        if 'cart_order_id' in self.request.session:
            cart_order_id = self.request.session['cart_order_id']
            order = Orders.objects.get(id=cart_order_id)
            print('payments order: ', order)
            context['total_amount'] = order.total_amount
            context['stripe_amount'] = order.total_amount *100
        print(context)
        return context


@require_POST
def charge(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        order = None
        if 'cart_order_id' in request.session:
            cart_order_id = request.session['cart_order_id']
            order = Orders.objects.get(id=cart_order_id)
        del request.session['cart_order_id']

        if order is None:
            redirect('PaymentsApp:payment-failure')
        description = 'Products Payment Amount of $ {}'.format(order.total_amount)
        charge = stripe.Charge.create(
            amount=round(order.total_amount*100),
            currency='usd',
            description=description,
            source=request.POST['stripeToken']
        )

        cart = Cart(request)
        order.has_paid = True
        order.save()
        send_order_email(order.customer.user.email, order.tracking_id, request)
        cart.clear()
        return render(request, 'FullStackApp/cart_success.html')


class PaymentFailure(TemplateView):
    template_name = 'payments/Failure.html'
