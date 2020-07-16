"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')8l*$#2jbu^c+34-8o#5dvwd$1m@1^12)&ypzy5*l@j35e-jsp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    'iot',
    'panel',
    'corsheaders',
    'api',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates",],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mqtt',
        'USER': 'root',
        'PASSWORD': '12345',
        'HOST': '127.0.0.1',
        'PORT': 3306
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'iotmqtt',
#         'USER': 'root',
#         'PASSWORD': '12345@ASDfg',
#         'HOST': '127.0.0.1',
#         'PORT': 3306
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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





AUTHENTICATION_BACKENDS = [
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'


ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'

STATIC_DIR = os.path.join(BASE_DIR,'static')
MEDIA_DIR = os.path.join(BASE_DIR,'media')


STATICFILES_DIRS = [STATIC_DIR,]
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'
CORS_ORIGIN_ALLOW_ALL = True


LOGIN_URL = 'panel/login'
LOGIN_REDIRECT_URL = 'panel'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'panel/login'

SOCIAL_AUTH_FACEBOOK_KEY = "289601318914389"        # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = "0f369c1a826be85976e6c1f4f0f93885"  # App Secret
SOCIAL_AUTH_FACEBOOK_API_VERSION = '2.8'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False
RAISE_EXCEPTIONS = False


SOCIAL_AUTH_GITHUB_KEY = "5020f5d701963e56c832"        # App ID
SOCIAL_AUTH_GITHUB_SECRET = "7d5aded97f28d91d00c344fa1ad8c46887094d55"  # App Secret





SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'panel.pipeline.save_to_group',
)
USE_X_FORWARDED_HOST = True



STRIPE_SECRET_KEY = 'sk_test_51GzOrkGyc8rsAgg7JYSyTkzCBXcBwfiZZUZN7GaZEmQajNARVF5ozQp4ItMeV7cA9U1ApbB4VEmnYWgDVn3ddEr200JiXGZCy7'
STRIPE_PUBLISHABLE_KEY = 'pk_test_51GzOrkGyc8rsAgg7nnTVJhJEHdVUjyRq9aDT1keBo8zqspDfuKBnyNPl5nlv9ic4QhJs6MMsz9jyy0pi85D5fJws002RN059uF'

