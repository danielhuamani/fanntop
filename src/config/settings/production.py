from .base import *

DEBUG = False

ALLOWED_HOSTS = ENV.get('CORS', [])

STATIC_ROOT = ENV.get('STATIC_ROOT')

STATIC_URL = ENV.get('STATIC_URL')

INSTALLED_APPS += [

]

MEDIA_ROOT = os.path.join(BASE_DIR, 'MEDIA_ROOT')

MEDIA_URL = os.path.join(BASE_DIR, 'MEDIA_URL')