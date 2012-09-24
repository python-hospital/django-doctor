from django.utils.datastructures import SortedDict
from django.views.debug import cleanse_setting


def cleanse_dictionary(dictionary):
    """
    Cleanse sensitive values in a dictionary.
    """

    cleansed_dictionary = SortedDict()

    for key, val in dictionary.iteritems():
        cleansed_dictionary[key] = cleanse_setting(key, val)

    return cleansed_dictionary
