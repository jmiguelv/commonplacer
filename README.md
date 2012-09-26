The Commonplacer
================

Django application for the creation of literary editions.

Testing registration
--------------------

  EMAIL_HOST = 'localhost'
  EMAIL_PORT = 9025
  EMAIL_HOST_USER = ''
  EMAIL_HOST_PASSWORD = ''
  EMAIL_USE_TLS = False
  DEFAULT_FROM_EMAIL = 'email@commonplacer' 

  python -m smtpd -n -c DebuggingServer localhost:9025
