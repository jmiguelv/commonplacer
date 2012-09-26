DEBUG = True

ADMINS = ()

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'dev.db'
            }
        }

STATIC_URL = '/static/'
TINYMCE_JS_URL = STATIC_URL + 'tiny_mce/tiny_mce_src.js'
TINYMCE_COMPRESSOR = False

EMAIL_HOST = 'localhost'
EMAIL_PORT = 9025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'email@commonplacer'
