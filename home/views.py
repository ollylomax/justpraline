from django.shortcuts import render, redirect, reverse, get_object_or_404
from products.models import Product
from contact.forms import ReviewForm
from contact.models import Review
from accounts.models import UserProfile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

def index(request):
    """ Simple route to return the Index template """
    # Filter products by is_new boolean
    products = Product.objects.filter(is_new=True)
    if request.user.is_authenticated:
        try:
            current_review = Review.objects.get(user_id=request.user)
        except Review.DoesNotExist:
            current_review = None
    else:
        current_review = None

    # Create new object by combining current user review object with
    # object excluding is_approved boolean, then ordering new object
    # with current user review as first index
    if Review.objects.filter(user_id=request.user.id):
        review_concat = Review.objects.filter(
            user_id=request.user.id) | Review.objects.exclude(
                is_approved=False)
        reviews = review_concat.order_by(Case(When(
            user_id=request.user.id, then=0), default=1))

        paginator = Paginator(reviews, 2)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    # If no current user review exists then define review object excluding
    # is_approved boolean
    else:
        reviews = Review.objects.exclude(is_approved=False)
        paginator = Paginator(reviews, 2)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    if request.method == 'GET':
        
        form = ReviewForm()
        if request.user.username:
            form['first_name'].initial = request.user.first_name
            form['last_name'].initial = request.user.last_name
            form['user'].initial = request.user

    else:
        form = ReviewForm(request.POST)

        if Review.objects.filter(user_id=request.user.id):
            messages.error(request, f'You already submitted a review')
        else:
            if form.is_valid():
                bleh = form.save()
                if bleh.appear_anonymous:
                    bleh.first_name = 'Anonymous'
                    bleh.last_name = 'User'
                    bleh.save()
                else:
                    form.save()
                messages.success(request, 'Review Added - Pending Approval')
                return redirect(reverse('home'))
        
    context = {
            'products': products,
            'form': form,
            'current_review': current_review,
            'page_obj': page_obj,
        }

    return render(request, 'home/index.html', context)


# Require session decorator from django decorators.
@login_required()
def edit_review(request, review_id):

    review = get_object_or_404(Review, pk=review_id)
    products = Product.objects.filter(is_new=True)

    # Create new object by combining current user review object with
    # object excluding is_approved boolean, then ordering new object
    # with current user review as first index
    if Review.objects.filter(user_id=request.user.id):
        review_concat = Review.objects.filter(
            user_id=request.user.id) | Review.objects.exclude(
                is_approved=False)
        reviews = review_concat.order_by(Case(When(
            user_id=request.user.id, then=0), default=1))
        paginator = Paginator(reviews, 2)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    # If no current user review exists then define review object excluding
    # is_approved boolean
    else:
        reviews = Review.objects.exclude(is_approved=False)
        paginator = Paginator(reviews, 2)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            user_review = form.save()
            user_review.is_approved = False
            user_review.save()
            messages.success(request, 'Review Edited - Pending Approval')
            return redirect(reverse('home'))
        else:
            messages.error(request, 'Failed to Edit Review')
    else:
        form = ReviewForm(instance=review)

    template = 'home/index.html'
    context = {
        'form': form,
        'review': review,
        'page_obj': page_obj,
        'products': products,
    }

    return render(request, template, context)


# Require session decorator from django decorators.
@login_required()
def delete_review(request, review_id):

    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    messages.success(request, 'Deletion successful - Review Removed')

    return redirect(reverse('home'))