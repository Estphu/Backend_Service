from .base import *

# Dev Environement

DEBUG = True

# Dev Host

ALLOWED_HOSTS = ['localhost','127.0.0.1']

# Dev Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Dev REST settings

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100, 
}