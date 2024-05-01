from .base import *

DEBUG = False

ALLOWED_HOSTS = ['zym.pythonanywhere.com']

TEMPLATES = [
    {
        #'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'BACKEND': 'core.backends.CustomTemplate',
        'DIRS': [BASE_DIR, 'real_estate/backend/templates'],
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


configured_settings = vars()

configured_settings = { i: configured_settings[i] for i in configured_settings if i.isupper() }

