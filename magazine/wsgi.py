"""
WSGI config for magazine project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import site

site.addsitedir('/var/www/magazine.com/lib/python2.7/site-packages')

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/magazine.com/bin/magazine')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "magazine.settings")

application = get_wsgi_application()

print 'IMPORTING', __name__, 'from', __file__
