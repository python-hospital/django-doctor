from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Test various file storage operations, to ensure that integrations (with ie.
    Amazon S3) is working properly.
    """

    help = 'Test file storage operations.'

    def handle(self, *args, **options):

        verbosity = int(options.get('verbosity', 1))
        filename = 'storage_test'

        if verbosity > 0:
            self.stdout.write('Storage used: %s\n' % settings.DEFAULT_FILE_STORAGE)

        # Create a file
        default_storage.save(filename, ContentFile('We are testing, 1 2 three.'))

        # Check for existence
        file_exists = default_storage.exists(filename)

        if verbosity > 0:
            self.stdout.write('Does newly created file exist? %s\n' % file_exists)

        # Read back the file
        f = default_storage.open(filename, 'r')
        file_contents = f.read()
        f.close()

        if verbosity > 0:
            self.stdout.write('Contents: "%s"\n' % file_contents)

        # Delete the file
        default_storage.delete(filename)
        file_exists = default_storage.exists(filename)

        if verbosity > 0:
            self.stdout.write('Does file exist after deletion? %s\n' % file_exists)
