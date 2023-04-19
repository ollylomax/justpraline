from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product
from .forms import ProductForm
from .custom_decorators import superuser_required


def all_products(request):
    """ Route for all products, including sorting and search queries. Get all
    products from Product object, initialise variables with None values. If
    category is in GET request, filter products object by category selected in
    template and reassign variable. If query is in GET request then assign
    requested query to variable and filter product names and descriptions by
    it, then reassign original variable with the filtered results. Pass
    product variable, categories and query back to the template."""

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'query' in request.GET:
            query = request.GET['query']
            if not query:
                messages.error(
                    request, "You must type something in the Search field")
                return redirect(reverse('products'))

            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'query': query,
        'categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ Route to show product details by receiving product id from path, using
    it to get the corresponding object from the Product model and assigning to
    a variable. Pass the variable back to the template. """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


# Require session decorator from django decorators.
@login_required
# Require superuser decorator from my custom decorators.
@superuser_required
def add_product(request):
    """ View to create a new print product, if request is POST initialise a
    ProductForm with the post and file requests, and if valid then save to
    variable. If invalid then send toast message and reverse to product detail
    page passing back the product id.

    If request is GET then initialise an empty ProductForm into the same
    variable name, pass to the template and render.
    """

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Addition Successful - product added')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Invalid Form - failed addition')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


# Require session decorator from django decorators.
@login_required
# Require superuser decorator from my custom decorators.
@superuser_required
def edit_product(request, product_id):
    """ Edit an existing print product by receiving product id from url path,
    searching Product model using the product id and returning the product to a
    variable. Instantiate a ProductForm with the variable set above and pass
    both the form and the variable to the template.

    If request is POST then check form for validity and if valid then save,
    sending a toast success message and reversing to product detail template
    passing the product id back as an argument. If invalid then send toast
    error message.
    """

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edit Successful - changes made')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Invalid Form - failed edit')
    else:
        form = ProductForm(instance=product)

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


# Require session decorator from django decorators.
@login_required
# Require superuser decorator from my custom decorators.
@superuser_required
def delete_product(request, product_id):
    """ Delete an existing print product by receiving product id from url path,
    searching Product model using the product id and returning the product to a
    variable. Delete the product, send toast success message and reverse to
    product view.
    """

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Deletion successful - product removed')

    return redirect(reverse('product'))
