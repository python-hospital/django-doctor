from django.core.management.base import BaseCommand

from doctor.services.storage import StorageServiceCheck


class Command(BaseCommand):
    """
    Test various file storage operations, to ensure that integrations (with ie.
    Amazon S3) is working properly.
    """

    help = 'Test file storage operations.'

    def handle(self, *args, **options):

        verbosity = int(options.get('verbosity', 1))

        # Check the status
        service_check = StorageServiceCheck()
        statuses = service_check.status()

        # Iterate over the backends, print status
        for storage_name, info in statuses.iteritems():

            if verbosity > 0:
                self.stdout.write('%s\n' % storage_name)
                self.stdout.write('%s\n\n' % info['message'])
