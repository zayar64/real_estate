from .base import *

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

configured_settings = vars()

configured_settings = { i: configured_settings[i] for i in configured_settings if i.isupper() }

