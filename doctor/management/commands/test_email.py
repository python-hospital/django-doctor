from django.contrib.sites.models import Site
from django.core.mail import mail_admins
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Test the sending of email with the mail_admins command.
    """

    help = 'Test sending of email.'

    def handle(self, *args, **options):

        verbosity = int(options.get('verbosity', 1))

        message = 'This is a test mail from %(site_name)s. If you see this, mail is working :)' % {
            'site_name': Site.objects.get_current().name,
        }

        try:
            mail_admins('Test mail', message, fail_silently=False)

            if verbosity > 0:
                self.stdout.write('Mail successfully sent to admins.\n')

        except Exception as exc:
            self.stderr.write('Sending test mail failed! Exception was: %s\n' % str(exc))
