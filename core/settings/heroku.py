"""
Django settings for core project when deployed on heroku.
"""

import os
from .base import *
import django_heroku

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
DEBUG = int(os.environ.get("DEBUG", default=1))

django_heroku.settings(locals())
