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


class HealthCheckLoader(unittest.TestLoader):
    """Encapsulate HealthCheck loading.

    This is a special TestLoader which makes sure instances are actually
    health checks.

    .. warning::

       Since this loader can be called with arguments provided by users (GET
       requests), **we have to make sure user input is safe**.
       As an example, we can't accept to load health checks from any callable,
       because this callable could be anything.

    """
    def is_health_check(self, value):
        """Return True if ``value`` is an health check.

        Proxy to :py:attr:``
        Tests ``is_healthcheck`` attribute of ``value``.

        """

        try:
            return value.is_healthcheck
        except AttributeError:
            return False

    def filter_suite(self, suite):
        """Return copy of TestSuite where only health checks remain."""
        if isinstance(suite, unittest.TestSuite):
            suite_copy = self.suiteClass()
            for sub in suite:
                if isinstance(sub, unittest.TestSuite):
                    suite_copy.addTest(self.filter_suite(sub))
                else:
                    if self.is_health_check(sub):
                        suite_copy.addTest(sub)
        elif self.is_health_check(suite):
            suite_copy = suite.copy()
        return suite_copy

    def loadTestsFromModule(self, module):
        suite_tree = super(HealthCheckLoader, self).loadTestsFromModule(module)
        return self.filter_suite(suite_tree)

    def loadTestsFromName(self, name, module=None):
        """Same as unittest.TestLoader.loadTestsFromName, but restricted
        to health test objects, i.e. no callable allowed."""
        parts = name.split('.')
        if module:
            parts.insert(0, module)
        # First, retrieve a module.
        module_obj = None
        path_parts = []
        while parts:
            latest_part = parts.pop(0)
            path_parts.append(latest_part)
            path = '.'.join(path_parts)
            try:
                imported_obj = __import__(path, globals(), locals(), [], -1)
            except ImportError as module_exception:
                if not module_obj:
                    raise module_exception
                else:
                    path_parts.pop()  # Last part is not a module.
                    path = '.'.join(path_parts)
                    break
            else:
                if not module_obj:
                    module_obj = imported_obj
                else:
                    module_obj = getattr(module_obj, latest_part)
        # We got ``module_obj`` for ``path``.
        # Let's retrieve members.
        parts = name[len(path):].lstrip('.')
        if not parts:
            return self.loadTestsFromModule(module_obj)
        else:
            parts = parts.split('.')
        class_name = parts[0]
        try:
            class_obj = getattr(module_obj, class_name)
        except AttributeError as class_exception:
            raise ImportError("Couldn't load '%s'" % name)
        if not self.is_health_check(class_obj):
            raise  ImportError("'%s' is not a health check" % name)
        try:
            method_name = parts[1]
        except IndexError:
            return self.loadTestsFromTestCase(class_obj)
        else:
            try:
                method_obj = getattr(class_obj, method_name)
            except AttributeError:
                raise  AttributeError("'%s' is not a health check method" % name)
            return unittest.TestSuite([class_obj(method_name)])

    def loadTestsFromNames(self, names, module=None):
        raise NotImplementedError()


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
                            """:py:class:`doctor.HealthCheck` instance.""")

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
