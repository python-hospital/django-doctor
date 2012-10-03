import datetime

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class
from django.utils.datastructures import SortedDict

from doctor.conf import STORAGE_CLASSES
from doctor.services import BaseServiceCheck


class StorageServiceCheck(BaseServiceCheck):
    """
    Check the status of the storage backend.
    """

    name = 'Storage'
    #template = ''

    def get_status_message(self, storage_class_path):

        # Create an instance of the storage class
        storage = get_storage_class(storage_class_path)()

        filename = 'storage_test'
        test_content = 'We are testing, 1 2 3.'

        # Create a new file
        try:
            storage.save(filename, ContentFile(test_content))
        except Exception as exc:
            return 'Saving file failed: %s' % exc

        # Check for existence
        if not storage.exists(filename):
            return 'Could not find created file.'

        # Read back the file
        try:
            f = storage.open(filename, 'r')
            file_contents = f.read()
            f.close()
        except Exception as exc:
            return 'Read file failed: %s' % exc

        if file_contents != test_content:
            return 'Could not read back the test file contents properly.'

        # Delete the file
        storage.delete(filename)

        if storage.exists(filename):
            return 'Created file could not be deleted.'

        return 'Storage tests passed.'

    def status(self):

        storage_info = {}

        for storage_class_path in STORAGE_CLASSES:
            status_message = self.get_status_message(storage_class_path)

            # Create dictionary with status info
            storage_info[storage_class_path] = {
                'is_working': status_message == 'Storage tests passed.',
                'message': status_message,
                'settings': self.get_settings(),
            }

        return storage_info

    def get_settings(self):
        """
        Returns dictionary of relevant storage settings.
        """

        storage_settings = SortedDict({})
        relevant_settings = (
            'DEFAULT_FILE_STORAGE',
            'STATICFILES_STORAGE',
            'STATIC_ROOT',
            'STATIC_URL',
            'MEDIA_ROOT',
            'MEDIA_URL',
        )

        for key in relevant_settings:
            storage_settings[key] = getattr(settings, key, '')

        return storage_settings
