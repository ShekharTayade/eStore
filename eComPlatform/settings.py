"""
Django settings for eComPlatform project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

from decouple import config, Csv
import dj_database_url

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b976^1fl!%o^0y1v6#rq8xwzpzi)^m(fom($j9m)_j-m-jiq7d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Store ID
STORE_ID = 1

# Application definition

INSTALLED_APPS = [
	'eStore.apps.EstoreConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'django_extensions',
	'django.contrib.sites',
	'widget_tweaks',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.amazon',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.instagram',	
    'allauth.socialaccount.providers.twitter',
	
]

SITE_ID = 1
TEMPLATE_DEBUG = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eComPlatform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
				# `allauth` needs this from django
                'django.template.context_processors.request',
				'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'eComPlatform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-IN'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = True

NUMBER_GROUPING = (3, 2, 0)

ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_UNIQUE_EMAIL = True

#ACCOUNT_SIGNUP_FORM_CLASS = 'NextSteps.forms.SignUpForm'

SOCIALACCOUNT_EMAIL_REQUIRED = ACCOUNT_EMAIL_REQUIRED
#SOCIALACCOUNT_AUTO_SIGNUP = False

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'js_sdk',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        #'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.8',
    },
    
    
 'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
        
}


# Authentication Backends added for social media
AUTHENTICATION_BACKENDS = (

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

    'django.contrib.auth.backends.ModelBackend',
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIR = [
    os.path.join(BASE_DIR, 'static'),
]
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

LOGOUT_REDIRECT_URL = 'index'

LOGOUT_URL = 'logout'

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
LOGIN_REDIRECT_URL = 'checkSubscription'

LOGIN_URL = 'login'

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# Cookie expiry in 2 weeks
SESSION_COOKIE_AGE = 1209600

SOCIAL_AUTH_FACEBOOK_KEY = ''  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = ''  # App Secret

SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

DEFAULT_FROM_EMAIL = ''
EMAIL_SUBJECT_PREFIX = ''

MEDIA_URL = ('/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


MOULDING_ROOT = os.path.join(BASE_DIR, 'eStore/static/img/')
TMP_FILES = os.path.join(BASE_DIR, 'eStore/static/tmp/')
CSS_FILES = os.path.join(BASE_DIR, 'eStore/static/css/')
VENDOR_FILES = os.path.join(BASE_DIR, 'eStore/static/vendor/')
