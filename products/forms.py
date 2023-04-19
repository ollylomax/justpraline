from django import forms
from .models import Product, Category
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):
    """
    Product form class using Product model with all fields. Set image
    imagefield variable to use custom clearable file input widget from
    imported widgets. Get all objects from Category model and iterate
    through them applying friendly names instead of id to category choices.
    """

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        # Overwrite init method to make changes to fields.
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        # List comprehension to create list of tuples of friendly names
        #   associated with their category ids.
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        # Update category field on form to use friendly names for choices
        #   instead of id.
        self.fields['category'].choices = friendly_names
