"""
Django settings for shopday project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
from config.utils import get_env
from django.utils.translation import ugettext_lazy as _
import os
import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ENV = get_env(BASE_DIR)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV.get('SECRET_KEY')
URL_SITE = 'http://fanntop.com/'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', 'localhost']
INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'widget_tweaks',
    'sorl.thumbnail',
    # 'django_filters'
]

BASE_APPS = [
    'apps_base.custom_auth',
    'apps_base.customers',
    'apps_base.security',
    'apps_base.influencer',
    'apps_base.category',
    'apps_base.product',
    'apps_base.attribute',
    'apps_base.family',
    'apps_base.pages',
    'apps_base.cart',
    'apps_base.order',
    'apps_base.ubigeo',
    'apps_base.payment',
    'apps_base.configuration',
    'apps_base.form',
    'apps_base.shipping',
    'apps_base.promotion'
]

WEB_APPS = [
    'apps_web.web_cart',
    'apps_web.web_product'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + BASE_APPS + WEB_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                "django.template.context_processors.i18n",
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps_web.web_system.context_processors.category_processors',
                'apps_web.web_system.context_processors.pages_processors'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': ENV.get('DATABASE_NAME'),
        'HOST': ENV.get('DATABASE_HOST'),
        'USER': ENV.get('DATABASE_USER'),
        'PASSWORD': ENV.get('DATABASE_PASSWORD'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}
CORS_ORIGIN_WHITELIST = tuple(ENV.get('CORS'))
CSRF_TRUSTED_ORIGINS = tuple(ENV.get('CORS'))

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'es'
LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)

TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
AUTH_USER_MODEL = 'custom_auth.User'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


JWT_AUTH = {
   'JWT_RESPONSE_PAYLOAD_HANDLER': 'apps_base.security.utils.jwt_response_payload_handler',
   'JWT_ALLOW_REFRESH': True,
   'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300*12*24*7),
   # 'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=10),
}

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        }
    }
}

THUMBNAIL_DEBUG = True
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_REDIS_HOST = 'localhost'
THUMBNAIL_REDIS_PORT = 6379
THUMBNAIL_DUMMY = True


EMAIL_HOST = ENV.get('EMAIL_HOST')
EMAIL_HOST_USER = ENV.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = ENV.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = ENV.get('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = ENV.get('SERVER_EMAIL')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# REST_FRAMEWORK = {
#     'DEFAULT_FILTER_BACKENDS': (
#         'django_filters.rest_framework.DjangoFilterBackend',
#     ),
# }