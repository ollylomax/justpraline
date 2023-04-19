from django import forms
from .models import UserProfile

from allauth.account.forms import ChangePasswordForm, SignupForm, LoginForm


class CustomChangePasswordForm(ChangePasswordForm):
    """
    Class to update existing allauth password change form by passing it in as
    an argument. Define custom placeholders for each form field then iterate
    through the fields making custom modifications.
    """
    def __init__(self, *args, **kwargs):
        super(CustomChangePasswordForm, self).__init__(*args, **kwargs)

        # Define custom placeholders
        placeholders = {
            'oldpassword': 'Enter Current Password',
            'password1': 'Enter New Password',
            'password2': 'Confirm New Password',
        }

        # Add aria labels
        self.fields[
            'oldpassword'].widget.attrs['aria-label'] = 'Current Password'
        self.fields['password1'].widget.attrs['aria-label'] = 'New Password'
        self.fields[
            'password2'].widget.attrs['aria-label'] = 'Repeat New Password'

        # Iterate through every field.
        for field in self.fields:
            if self.fields[field].required:
                # Add an asterisk to placeholder text if field is required.
                placeholder = f'{placeholders[field]} *'
            else:
                # Remain unchanged if not required.
                placeholder = placeholders[field]
            # Apply new placeholder text.
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Apply custom styling to match stripe.
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # Remove all labels.
            self.fields[field].label = False


class CustomRegisterForm(SignupForm):
    """
    Class to update existing allauth sign up form by passing it in as an
    argument. Define custom placeholders for each form field, set a desired
    autofocus then iterate through the fields making custom modifications.
    """
    def __init__(self, *args, **kwargs):
        super(CustomRegisterForm, self).__init__(*args, **kwargs)

        # Define custom placeholders
        placeholders = {
            'email': 'Enter Email',
            'email2': 'Confirm Email',
            'username': 'Enter Username',
            'password1': 'Enter Password',
            'password2': 'Confirm Password',
        }

        # Set aria labels
        self.fields['email'].widget.attrs['aria-label'] = 'Enter Email'
        self.fields['email2'].widget.attrs['aria-label'] = 'Confirm Email'
        self.fields['username'].widget.attrs['aria-label'] = 'Enter Username'
        self.fields['password1'].widget.attrs['aria-label'] = 'Enter Password'
        self.fields[
            'password2'].widget.attrs['aria-label'] = 'Confirm Password'

        # Set field as autofocus on page load.
        self.fields['email'].widget.attrs['autofocus'] = True

        # Iterate through every field.
        for field in self.fields:
            if self.fields[field].required:
                # Add an asterisk to placeholder text if field is required.
                placeholder = f'{placeholders[field]} *'
            else:
                # Remain unchanged if not required.
                placeholder = placeholders[field]
            # Apply new placeholder text.
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Apply custom styling to match stripe.
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # Remove all labels.
            self.fields[field].label = False


class CustomLoginForm(LoginForm):
    """
    Class to update existing allauth login form by passing it in as an
    argument. Define custom placeholders for each form field, then if the
    field is not checkbox iterate through the fields making custom
    modifications.
    """
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        # Define custom placeholders.
        placeholders = {
            'login': 'Enter Username or Email',
            'password': 'Enter Password',
        }

        self.fields[
            'login'].widget.attrs['aria-label'] = 'Enter Username Or Email'
        self.fields['password'].widget.attrs['aria-label'] = 'Enter Password'

        # Iterate through every field.
        for field in self.fields:
            # Omit the checkbox field from the nested iteration.
            if field != 'remember':
                if self.fields[field].required:
                    # Add an asterisk to placeholder text if field is required.
                    placeholder = f'{placeholders[field]} *'
                else:
                    # Remain unchanged if not required.
                    placeholder = placeholders[field]
                # Apply new placeholder text.
                self.fields[field].widget.attrs['placeholder'] = placeholder
                # Apply custom styling to match stripe.
                self.fields[field].widget.attrs['class'] = 'stripe-style-input'
                # Remove all labels.
                self.fields[field].label = False


class UserProfileForm(forms.ModelForm):
    """
    Form class importing the UserProfile model, excluding user field then
    add placeholders and style classes, remove all labels and set autofocus on
    desired field.
    """
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define custom placeholders.
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'default_address_line1': 'Street Address 1',
            'default_address_line2': 'Street Address 2',
            'default_city': 'City',
            'default_county': 'County',
            'default_postcode': 'Postal Code',
            'default_phone_number': 'Phone Number',
        }

        # Set field as autofocus on page load.
        self.fields['first_name'].widget.attrs['autofocus'] = True

        # Iterate through every field.
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    # Add an asterisk to placeholder text if field is required.
                    placeholder = f'{placeholders[field]} *'
                else:
                    # Remain unchanged if not required.
                    placeholder = placeholders[field]
                    # Apply new placeholder text.
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # Apply custom styling to match stripe.
            self.fields[field].widget.attrs[
                'class'] = 'border-black rounded-0 profile-form-input'
            # Remove all labels.
            self.fields[field].label = False
