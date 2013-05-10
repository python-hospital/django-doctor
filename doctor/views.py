import datetime
import os
import socket
import sys
import unittest

from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.utils.datastructures import SortedDict
from django.utils.importlib import import_module
from django.views.debug import cleanse_setting
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from hospital.loading import HealthCheckLoader

from doctor.conf import TEMPLATE_CONTEXT
from doctor.services import load_service_classes
from doctor.utils import cleanse_dictionary

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

@never_cache
def health_check(request):
    """
    Basic health check view, returns plain text response with 200 OK response.
    Useful for external monitor systems.

    TODO: Actually check all the services before returning OK :)
    """

    # Check for allowed remote IP addresses or superuser status
    if not request.META.get('REMOTE_ADDR', '') in settings.INTERNAL_IPS:
        if not request.user.is_superuser:
            raise Http404('Allowed IP addresses or superusers only.')

    response = HttpResponse(content_type='text/plain')

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
    environ = cleanse_dictionary(os.environ)

    return render(request, 'doctor/technical_info.html', {
        'doctor': TEMPLATE_CONTEXT,
        'versions': SortedDict(versions),
        'environ': environ,
        'paths': sys.path,
    })

def force_server_error(request):
    """
    Raises an exception. Useful for testing Sentry, error reporting mails, etc.
    """

    # Reject non-superusers
    if not request.user.is_superuser:
        raise Http404('Superusers only.')

    raise Exception('This unhandled exception is here by design.')

    return HttpResponse('This should never show up.', content_type='text/plain')


class HealthCheckView(TemplateView):
    """Load a health check, run it and return result."""
    #: Name of the health_check argument captured in urlpatterns.
    health_check_url_kwarg = 'health_check'

    #: Root path for health check loader.
    #: Health checks will be loaded relative to this root, and limited to
    #: descendants.
    #: Empty string means: "allow capture of all health checks, whatever the
    #: module, i.e. including third-party packages." So, in most cases, you
    #: should provide a root.
    health_check_root = ''

    #: Health check loader.
    health_check_loader = HealthCheckLoader()

    #: Default override for template name.
    template_name = 'health_check.html'

    def get_health_check(self):
        """Getter for :py:attr:`health_check`."""
        try:
            return self._health_check
        except AttributeError:
            pass
        health_check = self.kwargs.get(self.health_check_url_kwarg, None)
        if not self.health_check_loader.is_health_check(health_check):
            path = health_check.strip('/').replace('/', '.')
            health_check = self.health_check_loader.loadTestsFromName(
                path, self.health_check_root)
        self._health_check = health_check
        return self._health_check

    def set_health_check(self, value):
        """Setter for :py:attr:`health_check`."""
        self._health_chech = value

    def del_health_check(self):
        """Deleter for :py:attr:`health_check`."""
        del self._health_check

    health_check = property(get_health_check,
                            set_health_check,
                            del_health_check,
                            """:py:class:`hospital.HealthCheck` instance.""")

    def get_health_check_result(self):
        """Getter for health_check_result, runs tests when first requested."""
        try:
            return self._health_check_result
        except AttributeError:
            self._health_check_result = self.run_health_check()
        return self._health_check_result

    health_check_result = property(get_health_check_result)

    def get(self, request, *args, **kwargs):
        self.run_health_check()
        return super(HealthCheckView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(HealthCheckView, self).get_context_data(**kwargs)
        kwargs.setdefault('health_check_result', self.health_check_result)
        return kwargs

    def render_to_response(self, context, **kwargs):
        if not self.health_check_result.wasSuccessful():
            kwargs['status'] = 500
        return super(HealthCheckView, self).render_to_response(context,
                                                               **kwargs)

    def run_health_check(self):
        result = unittest.TestResult()
        self.health_check.run(result)
        return result
