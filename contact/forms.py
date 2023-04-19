from django import forms
from .models import Messages


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
