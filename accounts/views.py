from django.shortcuts import (
    render,
    get_object_or_404,
    get_list_or_404,
    redirect,
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from checkout.models import Order
from .models import UserProfile
from .forms import UserProfileForm
from contact.models import Messages


# Require session decorator from django decorators.
@login_required
def profile(request):
    """ Profile page view matching current user session with user profile and
    passing it to the profile template """

    profile = get_object_or_404(UserProfile, user=request.user)

    template = 'accounts/profile.html'

    context = {
        'profile': profile,
    }

    return render(request, template, context)


# Require session decorator from django decorators.
@login_required
def edit_profile(request):
    """ View to update user profile by matching current user session with user
    profile, instantiating UserProfile form with current profile then updating
    on POST. Get associated User object and update first and last name to match
    profile. If GET request then instantiate UserProfile form with current
    profile."""

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            user_form = get_object_or_404(User, username=request.user)
            user_form.first_name = request.POST['first_name']
            user_form.last_name = request.POST['last_name']
            user_form.save()
            messages.success(request, 'Update Successful - changes made')

            return redirect('profile')
        else:
            messages.error(request, 'Invalid Form - failed to update')
    else:
        form = UserProfileForm(instance=profile)

    template = 'accounts/edit_profile.html'
    context = {
        'form': form,
        'profile': profile,
    }

    return render(request, template, context)


# Require session decorator from django decorators.
@login_required
def order_history(request):
    """ View to display Order History by matching current session with
    associated profile, setting a variable for all associated orders and
    passing both profile and orders to the template."""

    profile = get_object_or_404(UserProfile, user=request.user)

    orders = profile.orders.all()

    template = 'accounts/order_history.html'
    context = {
        'orders': orders,
        'profile': profile,
    }

    return render(request, template, context)


# Require session decorator from django decorators.
@login_required
def past_order(request, order_number):
    """ View to display a previous user order by passing order number from the
    template, get the order object by order number, save it to a variable then
    pass it back to the template."""

    order = get_object_or_404(Order, order_number=order_number)

    template = 'accounts/past_order.html'
    context = {
        'order': order,
    }

    return render(request, template, context)


# Require session decorator from django decorators.
@login_required
def message_centre(request):
    """ View to display previously submitted user contact messages by checking
    if there are messages in the Message object filtered by current user
    session. Conditionally save filtered list of objects to a variable if
    messages exist then pass it to template."""

    if not Messages.objects.filter(user=request.user).exists():
        user_messages = None
    else:
        user_messages = get_list_or_404(Messages, user=request.user)

    template = 'accounts/messages.html'
    context = {
        'user_messages': user_messages,
    }

    return render(request, template, context)


# Require session decorator from django decorators.
@login_required
def past_message(request, message_id):
    """ View to display a previously submitted user contact message by passing
    message id from the template, get the message object by message id and
    save it to a variable. Check if the user from user session matches the user
    in message variable, and if so pass it back to the template."""
    message = get_object_or_404(Messages, pk=message_id)

    if request.user == message.user:

        template = 'accounts/past_message.html'
        context = {
            'message': message,
        }

        return render(request, template, context)
    else:
        messages.error(request, 'Invalid Message')
        return redirect(message_centre)
