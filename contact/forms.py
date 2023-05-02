from django import forms
from .models import Messages, Review


class ContactForm(forms.ModelForm):
    """
    Contact form using Messages model with hidden user field using widgets.
    """
    class Meta:
        model = Messages
        widgets = {
            'user': forms.HiddenInput(),
        }
        fields = (
            'user', 'first_name', 'last_name',
            'email', 'subject', 'message')


class ReviewForm(forms.ModelForm):
    """
    Review form using Messages model with hidden user field using widgets.
    """
    class Meta:
        model = Review
        widgets = {
            'user': forms.HiddenInput(),
            'is_approved': forms.HiddenInput(),
        }
        fields = (
            'user', 'first_name', 'last_name',
            'is_approved', 'appear_anonymous', 'review')
