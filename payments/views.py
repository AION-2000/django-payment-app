# payments/views.py

import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views import View  # The essential import for class-based views
from django.utils.decorators import method_decorator
from .models import Payment, Transaction
from .forms import PaymentForm
import json
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Set the Stripe API key from your settings
stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentView(View):
    """
    Handles the payment process. First, it shows the amount form.
    On POST, it creates a Stripe PaymentIntent and then shows the payment element.
    """
    template_name = 'payments/payment.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Display the initial payment form with the amount field."""
        form = PaymentForm()
        return render(request, self.template_name, {
            'form': form, 
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        })
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        Handles the form submission. If it's the first submission (amount),
        it creates a PaymentIntent. If it's the second submission (payment details),
        it confirms the payment.
        """
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = int(form.cleaned_data['amount'] * 100)  # Convert to cents for Stripe
            
            try:
                # Create a PaymentIntent with the order amount and currency.
                # NOTE: We have REMOVED the 'payment_method_types' parameter.
                # This allows Stripe's PaymentElement to automatically show only
                # the payment methods you have activated in your Stripe dashboard.
                intent = stripe.PaymentIntent.create(
                    amount=amount,
                    currency='usd',
                    metadata={
                        'user_id': request.user.id,
                        'email': request.user.email,
                    }
                )
                
                # Create a payment record in the database
                payment = Payment.objects.create(
                    user=request.user,
                    amount=form.cleaned_data['amount'],
                    currency='USD',
                    status='pending',
                    stripe_payment_intent_id=intent.id
                )
                
                # Return the client secret and payment ID to the frontend
                return JsonResponse({
                    'client_secret': intent.client_secret,
                    'payment_id': str(payment.id)
                })
            except stripe.error.StripeError as e:
                # Log the detailed Stripe error for debugging
                logger.error(f"Stripe error: {str(e)}")
                # Return a JSON error response with the specific message from Stripe
                return JsonResponse({'error': str(e)}, status=400)
            
        # If the form is invalid (e.g., reCAPTCHA failed), return validation errors
        return JsonResponse({'error': 'Invalid form data.', 'details': form.errors}, status=400)


class PaymentSuccessView(View):
    """
    Displays a success message after a payment is completed.
    """
    template_name = 'payments/success.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        payment_id = request.GET.get('payment_id')
        if payment_id:
            try:
                payment = Payment.objects.get(id=payment_id, user=request.user)
                return render(request, self.template_name, {'payment': payment})
            except Payment.DoesNotExist:
                messages.error(request, "Payment not found.")
                return redirect('payments:payment')
        
        return redirect('payments:payment')


class PaymentFailureView(View):
    """
    Displays a failure message if a payment could not be completed.
    """
    template_name = 'payments/failure.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        payment_id = request.GET.get('payment_id')
        if payment_id:
            try:
                payment = Payment.objects.get(id=payment_id, user=request.user)
                return render(request, self.template_name, {'payment': payment})
            except Payment.DoesNotExist:
                messages.error(request, "Payment not found.")
                return redirect('payments:payment')
        
        return redirect('payments:payment')


@require_POST
@csrf_exempt
def stripe_webhook(request):
    """
    Listens for webhook events from Stripe to update the payment status in the database.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        # Verify the webhook signature to ensure the request is from Stripe
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {str(e)}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {str(e)}")
        return HttpResponse(status=400)
    
    # Handle the specific event types
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        handle_payment_success(payment_intent)
    elif event.type == 'payment_intent.payment_failed':
        payment_intent = event.data.object
        handle_payment_failure(payment_intent)
    elif event.type == 'charge.succeeded':
        charge = event.data.object
        handle_charge_success(charge)
    
    return HttpResponse(status=200)


def handle_payment_success(payment_intent):
    """Updates the payment status to 'completed' and creates a transaction record."""
    try:
        payment = Payment.objects.get(stripe_payment_intent_id=payment_intent.id)
        payment.status = 'completed'
        payment.save()
        
        # Create a transaction record for the successful payment
        Transaction.objects.create(
            payment=payment,
            transaction_type='payment',
            amount=payment.amount,
            stripe_transaction_id=payment_intent.charges.data[0].id
        )
        
        logger.info(f"Payment {payment.id} succeeded")
    except Payment.DoesNotExist:
        logger.error(f"Payment with Stripe ID {payment_intent.id} not found in database")


def handle_payment_failure(payment_intent):
    """Updates the payment status to 'failed'."""
    try:
        payment = Payment.objects.get(stripe_payment_intent_id=payment_intent.id)
        payment.status = 'failed'
        payment.save()
        
        logger.info(f"Payment {payment.id} failed")
    except Payment.DoesNotExist:
        logger.error(f"Payment with Stripe ID {payment_intent.id} not found in database")


def handle_charge_success(charge):
    """Updates the payment record with the Stripe charge ID."""
    try:
        payment = Payment.objects.get(stripe_payment_intent_id=charge.payment_intent)
        payment.stripe_charge_id = charge.id
        payment.save()
        
        logger.info(f"Charge {charge.id} succeeded for payment {payment.id}")
    except Payment.DoesNotExist:
        logger.error(f"Payment with Stripe Payment Intent ID {charge.payment_intent} not found in database")