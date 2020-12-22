"""
Django settings for core project when deployed on heroku.
"""

import os
from .base import *
import django_heroku

django_heroku.settings(locals())
