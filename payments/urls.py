from django.urls import path
from .views import PaymentView, PaymentSuccessView, PaymentFailureView, stripe_webhook

app_name = 'payments'

urlpatterns = [
    path('', PaymentView.as_view(), name='payment'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failure/', PaymentFailureView.as_view(), name='failure'),
    path('webhook/', stripe_webhook, name='webhook'),
]