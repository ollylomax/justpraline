from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    User profile model for profile, order history, artwork and messages views
    with one-to-one field linking to built-in User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=80, null=True, blank=True)
    last_name = models.CharField(max_length=80, null=True, blank=True)
    default_address_line1 = models.CharField(
        max_length=80, null=True, blank=True)
    default_address_line2 = models.CharField(
        max_length=80, null=True, blank=True)
    default_city = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(
        blank_label='Country', null=True, blank=True)
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True)

    # String method for UserProfile class.
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Function to create or update the user profile.
    """
    # Create profile from the user parameter passed in.
    if created:
        UserProfile.objects.create(user=instance)
    # Save profile if existing user.
    instance.userprofile.save()
