from django.conf import settings
from decimal import Decimal
from django.shortcuts import get_object_or_404
from products.models import Product, Category


def cart_contents(request):
    """All page view to calculate contents of cart by initialising an empty
    list variable as well as initial values for cost variables. Get the current
    cart session then iterate over the contents calculating the total cost and
    quantity then appending to the empty list. Conditionally check if the cart
    meets the free delivery requirements and redefine delivery variable if so.
    Return all the updated variables and the cart items list."""

    cart_items = []
    total = 0
    product_count = 0
    delivery = 0
    delivery_dearth = 0

    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if cart_items:
        if total < settings.DELIVERY_THRESHOLD:
            delivery = total * Decimal(
                settings.DELIVERY_PERCENT / 100) + settings.DELIVERY_CHARGE
            delivery_dearth = settings.DELIVERY_THRESHOLD - total
        else:
            delivery = 0
            delivery_dearth = 0

    grand_total = delivery + total

    nav_categories = Category.objects.all()

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'delivery_dearth': delivery_dearth,
        'delivery_threshold': settings.DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'nav_categories': nav_categories,
    }

    return context
