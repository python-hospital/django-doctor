from django.core.management.base import BaseCommand

from doctor.services.email import EmailServiceCheck


class Command(BaseCommand):
    """
    Test the sending of email with the mail_admins command.
    """

    help = 'Test sending of email.'

    def handle(self, *args, **options):

        verbosity = int(options.get('verbosity', 1))
        
        # Use the email service check test method
        service_check = EmailServiceCheck()

        try:
            # Try to send an email to admins
            status = service_check.send_test_email()

            if verbosity > 0:
                self.stdout.write('Mail successfully sent to admins.\n')

        except Exception as exc:
            self.stderr.write('Sending test mail failed! Exception was: %s\n' % str(exc))
