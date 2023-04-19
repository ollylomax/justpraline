from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import ContactForm
from contact.models import Messages
from accounts.models import UserProfile

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail

from django.conf import settings


def contact(request):
    """
    Contact view where if request is GET then an empty ContactForm is
    initialised with pre-filled fields if there is a current user session
    and form is passed to template.

    If request is POST then a ContactForm is initialised from the post
    request and checked if valid. If valid then contact emails are assigned
    to corresponding variables and packaged in either a user email or company
    email. Emails are mass sent with exception handler.
    """

    if request.method == 'GET':
        form = ContactForm()
        if request.user.username:
            form['first_name'].initial = request.user.first_name
            form['last_name'].initial = request.user.last_name
            form['email'].initial = request.user.email
            form['user'].initial = request.user

    else:
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

            context = {
                'form': form,
            }
            subject = render_to_string(
                'contact/contact_email/contact_email_subject.txt', context)
            customer_email_body = render_to_string(
                'contact/contact_email/contact_confirmation_email_body.txt', context)
            company_email_body = render_to_string(
                'contact/contact_email/contact_from_email_body.txt', context)

            customer_email = (
                subject,
                customer_email_body,
                settings.VENTURE_PRESS_EMAIL,
                [form['email'].value()]
            )
            company_email = (
                subject,
                company_email_body,
                settings.VENTURE_PRESS_EMAIL,
                [settings.VENTURE_PRESS_EMAIL]
            )
            try:
                send_mass_mail(
                    (customer_email, company_email), fail_silently=False)
            except Exception as e:
                messages.error(request, f'Error: {e}')
                return HttpResponse(status=500)
            return redirect('success')

    return render(request, "contact/contact.html", {'form': form})


def success(request):
    """
    Simple success view which gets the current user from session and
    assigns a variable from the profile found in UserProfile model.
    Sends a toast success message and renders success template passing
    the user variable.
    """
    user = get_object_or_404(UserProfile, user=request.user)
    messages.success(request, "Your contact request has been received")

    return render(request, "contact/success.html", {'user': user})


# Require session decorator from django decorators.
@login_required()
def edit_message(request, message_id):
    """ Edit an existing user message by receiving message id from url path,
    searching Messages model by primary key and returning the message to a
    variable. Instantiate a ContactForm with the variable set above and pass
    both the form and the variable to the template. If request is POST then
    check form for validity and if valid then save.
    """

    message = get_object_or_404(Messages, pk=message_id)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edit Successful - changes made')
            return redirect(reverse('past_message', args=[message.id]))
        else:
            messages.error(request, 'Invalid Form - failed edit')
    else:
        form = ContactForm(instance=message)

    template = 'contact/edit_message.html'
    context = {
        'form': form,
        'message': message,
    }

    return render(request, template, context)


# Require session decorator from django decorators.
@login_required()
def delete_message(request, message_id):
    """ Delete an existing user message by receiving message id from url path,
    searching Messages database by primary key and returning the message to a
    variable. Delete message and send toast success message.
    """

    message = get_object_or_404(Messages, pk=message_id)
    message.delete()
    messages.success(request, 'Deletion successful - message removed')

    return redirect(reverse('message_centre'))
