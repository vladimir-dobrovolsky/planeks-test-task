"""
Django settings for core project when deployed on heroku.
"""

import os
from .base import *
import django_heroku

MIDDLEWARE += [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
DEBUG = int(os.environ.get("DEBUG", default=1))

django_heroku.settings(locals())
