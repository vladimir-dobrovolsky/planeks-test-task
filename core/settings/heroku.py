"""
Django settings for core project when deployed on heroku.
"""

import os
from .base import *
import django_heroku

MIDDLEWARE += [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

MEDIA_URL = "/tmp/"
MEDIA_ROOT = os.path.join(BASE_DIR, "tmp")

FILE_UPLOAD_PERMISSIONS = 0o644

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
DEBUG = int(os.environ.get("DEBUG", default=1))

HEROKU_MEDIA = True

django_heroku.settings(locals())
