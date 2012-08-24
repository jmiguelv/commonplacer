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
