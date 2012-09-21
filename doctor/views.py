import datetime
import os
import socket
import sys

from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.utils.datastructures import SortedDict
from django.utils.importlib import import_module
from django.views.debug import cleanse_setting

from doctor.conf import TEMPLATE_CONTEXT
from doctor.services import load_service_classes

# Fetch the socket name
socket_name = socket.gethostname()

# Load service health check classes
services = load_service_classes()


def index(request):
    """
    Various health checks, displayed as HTML.
    """

    # Reject non-superusers
    if not request.user.is_superuser:
        raise Http404('Superusers only.')

    return render(request, 'doctor/index.html', {
        'doctor': TEMPLATE_CONTEXT,
        'services': services,
    })

def health_check(request):
    """
    Basic health check view, returns plain text response with 200 OK response.
    Useful for external monitor systems.

    TODO: Should we limit this to some extent? (maybe INTERNAL_IPS?)
    """

    response = HttpResponse(content_type='text/plain')
    response['Cache-Control'] = 'no-cache'

    # Generate message and hit the database
    msg = '%(domain)s running on %(socket_name)s is OK at %(datetime)s' % {
        'domain': Site.objects.get_current().domain,
        'socket_name': socket_name,
        'datetime': datetime.datetime.now()
    }
    response.write(msg)

    return response

def technical_info(request):
    """
    Version numbers for applications in use.
    Borrowed from the django-debug-toolbar.
    """

    # Reject non-superusers
    if not request.user.is_superuser:
        raise Http404('Superusers only.')

    # Module version information
    versions = [('Python', '%d.%d.%d' % sys.version_info[:3])]

    for app in list(settings.INSTALLED_APPS) + ['django']:
        name = app.split('.')[-1].replace('_', ' ').capitalize()
        app = import_module(app)
        if hasattr(app, 'get_version'):
            get_version = app.get_version
            if callable(get_version):
                version = get_version()
            else:
                version = get_version
        elif hasattr(app, 'VERSION'):
            version = app.VERSION
        elif hasattr(app, '__version__'):
            version = app.__version__
        else:
            continue
        if isinstance(version, (list, tuple)):
            version = '.'.join(str(o) for o in version)
        versions.append((name, version))
        versions = sorted(versions, key=lambda version: version[0])

    # Return environment variables with sensitive content cleansed
    environ = {}
    for key, val in os.environ.iteritems():
        environ[key] = cleanse_setting(key, val)

    return render(request, 'doctor/technical_info.html', {
        'doctor': TEMPLATE_CONTEXT,
        'versions': SortedDict(versions),
        'environ': environ,
        'paths': sys.path,
    })

def force_server_error(request):
    """
    Raises an exception. Useful for testing Sentry, error reporting mails.
    """

    # Reject non-superusers
    if not request.user.is_superuser:
        raise Http404('Superusers only.')

    raise Exception('This unhandled exception is here by design.')

    return HttpResponse('This should never show up.', content_type='text/plain')
