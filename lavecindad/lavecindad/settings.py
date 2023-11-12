"""
Django settings for lavecindad project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from django.contrib.messages import constants as mensajes_de_error

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-fhn9md=@mm*)clz#rx2x)9(jas)p@#zhv_phi(r^-b%70z5gqx'

DEBUG = True

ALLOWED_HOSTS = ['755a-186-78-183-213.ngrok-free.app', 'localhost', '127.0.0.1']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vecindad',
    'crispy_forms',
    
   
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    
]

ROOT_URLCONF = 'lavecindad.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['template'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lavecindad.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lavecindad',
        'USER': 'lavecindad',
        'PASSWORD': 'lavecindad',
    }
}

# Resto de la configuración de validación de contraseñas, internacionalización, archivos estáticos y más.

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Nueva configuración para el directorio de archivos estáticos en producción

# Resto de la configuración ...

if not DEBUG:
    # En un entorno de producción, servimos archivos estáticos usando la configuración de STATIC_ROOT
    # Configura tu servidor web para que sirva los archivos estáticos desde esta ubicación.
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'vecindad/static'),
        os.path.join(BASE_DIR, 'vecindad/static/img'),
        os.path.join(BASE_DIR, 'vecindad/static/js'),
    ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'vecindad.UsuarioPersonalizado'



LOGIN_URL = 'iniciar_sesion'  # Nombre de la URL de inicio de sesión
LOGOUT_REDIRECT_URL = 'iniciar_sesion'  # Nombre de la URL a la que se redirige después de cerrar sesión

MESSAGE_TAGS ={

    mensajes_de_error.DEBUG: 'debug',
    mensajes_de_error.INFO: 'info',
    mensajes_de_error.SUCCESS: 'success',
    mensajes_de_error.WARNING: 'warning',
    mensajes_de_error.ERROR: 'danger',

}

# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'juntadevecinoslavecindad@gmail.com'
EMAIL_HOST_PASSWORD = 'siei fika czua bkdk'

# Configuración de OAuth 2.0
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '800406312850-69gbig8funi11j4lbgenu1jdclvl06do.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
