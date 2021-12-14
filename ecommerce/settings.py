from pathlib import Path

import django.core.mail.backends.console

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-a4!xdk@^0d#oo)3_y-u%vzo&9+x)o1)o%e&%i$5+!_5=&^is@b'

DEBUG = True

ALLOWED_HOSTS = ['yourdomain.com', '127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    'store.apps.StoreConfig',
    'basket.apps.BasketConfig',
    'account.apps.AccountConfig',
    'payment.apps.PaymentConfig',
    'orders.apps.OrdersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.categories',  # add new
                'basket.context_processors.basket',  # add new
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User model
AUTH_USER_MODEL = 'account.UserBase'
LOGIN_REDIRECT_URL = '/account/dashboard'
LOGIN_URL = '/account/login/'

# Email setting
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Stripe
STRIPE_ENDPOINT_SECRET = 'whsec_QjdTlKeAZRJZCI2UJEzgoRoREZSzoAtU'
PUBLISHABLE_KEY = 'pk_test_51K6LvrAditzYOocIsiB0wm5aky3z19XQRfqt4rwnivuZ65JzxiWadGoWGGgF9Bqem6nqXMtVuuPKlTMsgLgnW93M00x09R61en'
SECRET_KEY = 'sk_test_51K6LvrAditzYOocI1eVdxbGnM8byAMYLW7Pm92I0zkYVKgNIZYx3Wn23OFx5dZf19lmbYV5hzZkQHqvuOlUFPQD500mukpiWGe'

# basket session ID
BASKET_SESSION_ID = 'basket'
