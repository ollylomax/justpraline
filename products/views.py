from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product
from .forms import ProductForm
from contact.models import ProductReview
from contact.forms import ProductReviewForm
from .custom_decorators import superuser_required
from django.core.paginator import Paginator


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
    all_reviews = ProductReview.objects.filter(product=product)
    
    if request.user.is_authenticated:
        if all_reviews.filter(user_id=request.user):
            customer_review = get_object_or_404(all_reviews, user_id=request.user)
        else:
            customer_review = None

        product_reviews = all_reviews.filter(is_approved=True).exclude(user_id=request.user)
    else:
        customer_review = None
        product_reviews = all_reviews.filter(is_approved=True)

    paginator = Paginator(product_reviews, 2)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.method == 'GET':
        
        form = ProductReviewForm()
        form['product'].initial = product
        if request.user.username:
            form['first_name'].initial = request.user.first_name
            form['last_name'].initial = request.user.last_name
            form['user'].initial = request.user

    else:
        form = ProductReviewForm(request.POST)

        if form.is_valid():
            p_review = form.save()
            p_review.product = product
            p_review.save()
            messages.success(request, 'Product Review Added - Pending Approval')
            return redirect(reverse('product_detail', args=[product.id]))

    context = {
        'product': product,
        'form': form,
        'customer_review': customer_review,
        'page_obj': page_obj,
    }

    return render(request, 'products/product_detail.html', context)


# Require session decorator from django decorators.
@login_required()
def edit_product_review(request, product_id, product_review_id):

    in_edit = True
    product_review = get_object_or_404(ProductReview, pk=product_review_id)
    products = Product.objects.filter(is_new=True)
    product = get_object_or_404(Product, pk=product_id)
    all_reviews = ProductReview.objects.filter(product=product)
    
    if all_reviews.filter(user_id=request.user):
        customer_review = get_object_or_404(all_reviews, user_id=request.user)
    else:
        customer_review = None

    product_reviews = all_reviews.filter(is_approved=True).exclude(user_id=request.user)

    if request.method == 'POST':
        form = ProductReviewForm(request.POST, instance=product_review)
        if form.is_valid():
            user_review = form.save()
            user_review.is_approved = False
            user_review.save()
            in_edit = False
            messages.success(request, 'Review Edited - Pending Approval')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to Edit Review')
    else:
        form = ProductReviewForm(instance=product_review)

    template = 'products/product_detail.html'
    context = {
        'product': product,
        'form': form,
        'customer_review': customer_review,
        'product_reviews': product_reviews,
        'product_review': product_review,
        'in_edit': in_edit,
    }

    return render(request, template, context)


# Require session decorator from django decorators.
@login_required()
def delete_product_review(request, product_id, product_review_id):
    
    product = get_object_or_404(Product, pk=product_id)
    product_review = get_object_or_404(ProductReview, pk=product_review_id)
    product_review.delete()
    messages.success(request, 'Deletion successful - Product Review Removed')

    return redirect(reverse('product_detail', args=[product.id]))

# Require session decorator from django decorators.
@login_required()
def delete_review(request, review_id):

    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    messages.success(request, 'Deletion successful - Review Removed')

    return redirect(reverse('home'))

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

    return redirect(reverse('products'))
