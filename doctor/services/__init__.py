from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from doctor.conf import SERVICES


class BaseServiceCheck(object):
    """
    Base class for service check classes.

    TODO This is temporary, not happy with the current implementation.
    """

    # name = 'Base'
    # template = 'doctor/services/generic.html'

    def status(self):
        """
        Returns a dict of the status current.
        """

        raise NotImplementedError('Method not implemented in inherited class.')


def load_service_classes():
    """
    Load service classes defined in settings.
    Code inspired by django-debug-toolbar, thanks!
    """

    service_classes = []

    for service_path in SERVICES:

        try:
            dot = service_path.rindex('.')
        except ValueError:
            raise ImproperlyConfigured('%s is not a service check module.' % service_path)

        service_module, service_classname = service_path[:dot], service_path[dot + 1:]

        try:
            module = import_module(service_module)
        except ImportError as e:
            raise ImproperlyConfigured('Error importing service check %s: "%s' % (service_module, e))

        try:
            service_class = getattr(module, service_classname)
        except AttributeError:
            raise ImproperlyConfigured('Service module "%s" does not define a "%s" class' % (
                service_module, service_classname
            ))

        service_classes.append(service_class)

    return service_classes
