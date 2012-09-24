from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import get_connection
from django.core.mail import mail_admins
from django.utils.datastructures import SortedDict
from doctor.utils import cleanse_dictionary

from doctor.services import BaseServiceCheck


class EmailServiceCheck(BaseServiceCheck):
    """
    Check the status of the email settings.
    """

    name = 'Email'
    #template = ''

    def send_test_email(self):
        """
        Send a test email to the admins defined in settings.
        """

        message = 'This is a test mail from %(site_name)s. If you see this, mail is working :)' % {
            'site_name': Site.objects.get_current().name,
        }

        return mail_admins('Test mail', message, fail_silently=False)

    def status(self):
        """
        TODO Implement a connection test to the email backend.
        """

        email_info = {}
        is_mail_working = True

        # Create dictionary with status info
        email_info['default'] = {
            'is_working': is_mail_working,
            'message': 'Check mail using management command "test_email"',
            'settings': self.get_settings(),
        }

        return email_info

    def get_settings(self):
        """
        Returns dictionary of relevant storage settings, with sensitive
        variables cleansed.
        """

        email_settings = SortedDict({})
        relevant_settings = (
            'EMAIL_BACKEND',
            'EMAIL_HOST',
            'EMAIL_HOST_USER',
            'EMAIL_HOST_PASSWORD',
            'EMAIL_USE_TLS',
            'EMAIL_PORT',
        )

        for key in relevant_settings:
            email_settings[key] = getattr(settings, key, '')

        return cleanse_dictionary(email_settings)
