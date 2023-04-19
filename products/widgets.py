from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    """
    Custom widget inheriting the Clearable File Input widget from django.
    Set input text to empty string, change labels and initial text and set
    template to the custom widget html page in new template directory.
    """

    input_text = _('')
    clear_checkbox_label = _('Delete Image')
    initial_text = _('Product Image')

    template_name = (
        'products/custom_widget_templates/custom_clearable_file_input.html'
    )
