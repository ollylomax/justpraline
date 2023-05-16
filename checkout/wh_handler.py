from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail

from django.conf import settings

from products.models import Product
from accounts.models import UserProfile
from .models import Order, OrderLineItem

import time
import json


class main_handler:
    """Handler for stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_order_confirmation_email(self, order):
        """
        Function for when an order is placed to send a order confirmation
        email to user's email address based on txt templates.
        """
        subject = render_to_string(
            'checkout/order_confirmation_email/order_confirmation_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/order_confirmation_email/order_confirmation_body.txt',
            {'order': order, 'jp_email': settings.JP_EMAIL})
        # Takes four parameters, email subject, email body, from
        #   email and to email.
        send_mail(
            subject,
            body,
            settings.JP_EMAIL,
            [order.email]
        )

    def generic_handler(self, event):
        """
        Handler for a undefined webhook event.
        """
        return HttpResponse(
            content=f'Undefined webhook: {event["type"]}',
            status=200)

    def pi_succeeded_handler(self, event):
        """
        Stripe payment_intent.succeeded webhook handler
        """
        intent = event.data.object.retrieve(
            event.data.object.id, expand=["latest_charge"])
        pid = intent.id
        # JSON version of cart from intent
        cart = intent.metadata.cart
        # Save info checkbox boolean
        save_info = intent.metadata.save_info

        # print(intent.retrieve(pid, expand=["latest_charge"]))

        billing_details = intent.latest_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.latest_charge.amount / 100, 2)

        # Iterate through address to replace empty fields with None
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # If save info box checked then update profile through webhook
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = shipping_details.address.line1
                profile.default_street_address2 = shipping_details.address.line2
                profile.default_county = shipping_details.address.state
                profile.save()

        order_exists = False
        # Variable to increment for python sleep timer
        attempt = 1
        # Loop to try and find the order five times before moving on
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    city__iexact=shipping_details.address.city,
                    address_line1__iexact=shipping_details.address.line1,
                    address_line2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    cart_instance=cart,
                    payment_id=pid,
                )
                order_exists = True
                # Break out of the while loop if order is found
                break
            except Order.DoesNotExist:
                # Increment variable by 1
                attempt += 1
                # Python sleep timer
                time.sleep(1)
        if order_exists:
            self._send_order_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook: {event["type"]} | SUCCESS: Order exists',
                status=200)
        else:
            # Create the order in database using the stripe payment
            #   intent information
            order = None
            try:
                order = Order.objects.create(
                    user_profile=profile,
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    city=shipping_details.address.city,
                    address_line1=shipping_details.address.line1,
                    address_line2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    cart_instance=cart,
                    payment_id=pid,
                )
                for item_id, quantity in json.loads(cart).items():
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()

            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_order_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook: {event["type"]} | SUCCESS: Webhook order',
            status=200)

    def pi_payment_failed_handler(self, event):
        """
        Stripe payment_intent.payment_failed webhook handler
        """
        return HttpResponse(
            content=f'Webhook: {event["type"]}',
            status=200)
