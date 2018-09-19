from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

STATIC_ROOT = ''

STATIC_URL = '/static/'

INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions'
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'


CULQUI_PUBLIC_KEY_TEST = ENV.get('CULQUI_PUBLIC_KEY_TEST')
CULQUI_SECRET_KEY_TEST = ENV.get('CULQUI_SECRET_KEY_TEST')
