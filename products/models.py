from django.db import models
from django.core.validators import MinLengthValidator


class Type(models.Model):
    """
    Type model with name and image fields. Change tags plural for
    admin view.
    """

    name = models.CharField(max_length=254)
    description = models.TextField(max_length=254)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Tags(models.Model):
    """
    Tags model with name and image fields. Change tags plural for
    admin view.
    """
    class Meta:
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=254)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Category model with simple name and friendly name fields with friendly name
    not required. Change category plural for admin view.
    """
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    """
    Product modelincluding foreign key from Category model, basic charfields,
    text field with a min length validator for description, image field and
    decimal field and a paper size char field with choices.
    """

    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    edition = models.ForeignKey(
        'Type', null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tags')
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField(validators=[MinLengthValidator(150)])
    ingredients = models.TextField(max_length=254)
    allergens = models.TextField(max_length=254)
    nutritional = models.TextField(max_length=254)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)


    def __str__(self):
        return self.name
