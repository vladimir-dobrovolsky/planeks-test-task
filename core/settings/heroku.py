"""
Django settings for core project when deployed on heroku.
"""

import os
from .base import *
import django_heroku

MIDDLEWARE += [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

FILE_UPLOAD_PERMISSIONS = 0o644

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
DEBUG = int(os.environ.get("DEBUG", default=1))

HEROKU_MEDIA = os.environ.get("AWS_ACCESS_KEY_ID")
AWS = True

django_heroku.settings(locals())
