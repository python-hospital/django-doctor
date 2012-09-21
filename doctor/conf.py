from django.conf import settings

from . import __version__ as doctor_version


# Doctor template variables
TEMPLATE_CONTEXT = {
    'base_template': getattr(settings, 'DOCTOR_BASE_TEMPLATE', 'base.html'),
    'version': doctor_version,
}

# Installed service checks. You can override this in Django settings
SERVICES = getattr(settings, 'DOCTOR_SERVICES', (
    'doctor.services.cache.CacheServiceCheck',
    'doctor.services.celery.CeleryServiceCheck',
))
