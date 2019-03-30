from django.urls import path

from payments import views

app_name = 'PaymentsApp'

urlpatterns = [
path('', views.HomePageView.as_view(), name='home'),
path('', views.PaymentFailure.as_view(), name='payment-failure'),
path('charge', views.charge, name='payment-charge'),
    ]

