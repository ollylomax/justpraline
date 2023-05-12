from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Subjects tuple for subject choices field.
SUBJECTS = (
    ('GENERAL', 'General'),
    ('QUOTE', 'Quote'),
    ('COMPLAINT', 'Complaint'),
    ('PARTNERS', 'Partners'),
)


class Messages(models.Model):
    """
    Contact model for contact and success views including foreign key from
    User model, date time field, charfield with choices from tuple above,
    standard charfields, email field and textfield for the message content.
    """
    class Meta:
        # Change plural in admin
        verbose_name_plural = 'Messages'

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=15, null=False, blank=False)
    last_name = models.CharField(max_length=15, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    subject = models.CharField(
        max_length=10, choices=SUBJECTS, default='GENERAL')
    message = models.TextField(max_length=200, null=False, blank=False)


class Review(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=80, null=True, blank=True)
    last_name = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    appear_anonymous = models.BooleanField(null=False, blank=False, default=False)
    is_approved = models.BooleanField(null=False, blank=False, default=False)
    review = models.TextField(max_length=200, null=False, blank=False)


class ProductReview(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False)
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=80, null=True, blank=True)
    last_name = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    appear_anonymous = models.BooleanField(null=False, blank=False, default=False)
    is_approved = models.BooleanField(null=False, blank=False, default=False)
    product_review = models.TextField(max_length=500, null=False, blank=False)