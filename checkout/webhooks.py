from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.wh_handler import main_handler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """Communicate with stripe to listen for incoming webhooks"""
    # Setup keys from settings file
    endpoint_secret = settings.ENDPOINT_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
        # Generic exception
    except Exception as e:
        return HttpResponse(content=e, status=400)

    # Initialise my webhook handler
    handler = main_handler(request)

    # Map webhook events to corresponding handlers
    event_map = {
        'payment_intent.succeeded': handler.pi_succeeded_handler,
        'payment_intent.payment_failed': handler.pi_payment_failed_handler,
    }

    # Get the webhook type from Stripe
    event_type = event['type']

    # If there's a handler for it, get it from the event map
    # Otherwise use the generic handler
    event_handler = event_map.get(event_type, handler.generic_handler)

    # Call the event handler passing in the event as argument
    response = event_handler(event)
    return response
