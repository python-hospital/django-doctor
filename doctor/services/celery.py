from django.conf import settings

from doctor.services import BaseServiceCheck


class CeleryServiceCheck(BaseServiceCheck):
    """
    Check the status of Celery.
    """

    name = 'Celery'
    #template = ''

    def status(self):

        celery_info = {}

        if 'djcelery' in settings.INSTALLED_APPS:

            is_celery_working = False

            try:
                from celery.task.control import inspect

                insp = inspect()
                celery_stats = insp.stats()

                if celery_stats:
                    is_celery_working = True
                    celery_message = celery_stats
                else:
                    celery_message = 'No running Celery workers found.'

            except IOError as ex:
                celery_message = 'Could not connect to the backend: %s' % str(ex)
            except ImportError as ex:
                celery_message = str(ex)
            
            # Format the status messages
            if is_celery_working:
                for key, val in celery_message.iteritems():
                    celery_info[key] = {
                        'settings': val,
                        'is_working': is_celery_working,
                    }
            else:
                # Set the error message
                celery_info['default'] = {}
                celery_info['default']['is_working'] = is_celery_working
                celery_info['default']['message'] = celery_message

        return celery_info
