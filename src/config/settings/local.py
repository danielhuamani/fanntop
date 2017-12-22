from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

STATIC_ROOT = ''

STATIC_URL = '/static/'

INSTALLED_APPS += [

]


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'