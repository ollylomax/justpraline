from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from products.models import Product


def cart(request):
    """ Simple route to render the cart template """

    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ View to add or update the quantity of chosen products to cart by receiving
    item id from the template, using it to get the corresponding product and
    adding or updating their quantity to the cart variable then updating the
    session. Set a variable for the path from POST and redirect to previous path
    after adding/updating.
    """

    product = Product.objects.get(pk=item_id)
    if request.POST.get('quantity'):
        quantity = int(request.POST.get('quantity'))
    else:
        quantity = 1
    path = request.POST.get('path')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        if cart[item_id] + quantity > 10:
            messages.error(request, f'You cannot buy more than 10 boxes of {product.name} in a single order')
        else:
            cart[item_id] += quantity
            messages.success(request, f'Cart updated to {cart[item_id]} boxes of {product.name}')
    else:
        cart[item_id] = quantity
        if quantity == 1:
            messages.success(request, f'Added {quantity} box of {product.name} to your Cart')
        else:
            messages.success(request, f'Added {quantity} boxes of {product.name} to your Cart')

    request.session['cart'] = cart
    return redirect(path)


def quantity_amend(request, item_id):
    """View to amend the quantity of the chosen product by receiving the item
    id from the template, getting the corresponding product from the Product
    object and saving it to a variable. Get the quantity from the POST request
    and the cart from session if it exists, else create an empty object. Use
    conditional to update or delete products from the cart then update the cart
    session and redirect to cart view."""

    quantity = int(request.POST.get('quantity'))
    product = Product.objects.get(pk=item_id)
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[item_id] = quantity
        messages.success(request, f'Cart updated to {cart[item_id]} boxes of {product.name}')
    else:
        cart.pop(item_id)
        messages.success(request, f'Removed all boxes of {product.name} from your Cart')

    request.session['cart'] = cart
    return redirect(reverse('cart'))


def delete_from_cart(request, item_id):
    """View to remove the chosen product by receiving the item id from the
    template, getting the corresponding product from the Product object and
    saving it to a variable. Get the cart from session if it exists, else
    create an empty object. Delete product from the cart then update the cart
    session."""

    cart = request.session.get('cart', {})
    product = Product.objects.get(pk=item_id)
    
    try:
        cart.pop(item_id)
        messages.success(request, f'Removed all boxes of {product.name} from your Cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error when removing item: {e}')
        return HttpResponse(status=500)