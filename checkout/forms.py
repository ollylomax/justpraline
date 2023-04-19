from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    Form class importing the Order model and hiding the has_artwork boolean
    field using widgets.
    """
    class Meta:
        model = Order
        widgets = {
            'has_artwork': forms.HiddenInput(),
        }
        fields = ('full_name', 'email', 'phone_number',
                  'address_line1', 'address_line2',
                  'city', 'postcode', 'country',
                  'county', 'has_artwork')

    def __init__(self, *args, **kwargs):
        """
        Set custom placeholders and autofocus to full name. Iterate through all
        fields excluding the has_artwork boolean, apply placeholders, add
        custom stripe style classes and remove all labels.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Post Code',
            'city': 'City',
            'address_line1': 'Address Line 1',
            'address_line2': 'Address Line 2',
            'county': 'County',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field != 'country':
                if field != 'has_artwork':
                    if self.fields[field].required:
                        placeholder = f'{placeholders[field]} *'
                    else:
                        placeholder = placeholders[field]
                    self.fields[
                        field].widget.attrs['placeholder'] = placeholder
                    self.fields[
                        field].widget.attrs['class'] = 'stripe-style-input'
                    self.fields[field].label = False
