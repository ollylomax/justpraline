from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """ Get static files location from settings file """
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """ Get media files location from settings file """
    location = settings.MEDIAFILES_LOCATION
