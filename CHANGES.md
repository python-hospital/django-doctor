# Django Doctor Changelog

## 0.4.0 (2015-10-21)
* Now uses Python's `import_module`, drops support for Python < 2.7

## 0.3.0 (2015-07-06)
* Removed use of SortedDict, now uses OrderedDict available in Python >= 2.7
* Added support for new caches lookup introduced in Django 1.7, in favor of get_cache.
* Removed loading of url template tag from future, drops compatibility with Django 1.4

## 0.2.6 (2012-01-02)
* Handle exceptions when loading storage classes.
* Compatibility with Django < 1.4 URL config import.

## 0.2.5 (2012-12-05)
* Removed an unused template from PyPi package.

## 0.2.4 (2012-10-17)
* Added never_cache decorator to health check view.

## 0.2.3 (2012-10-12)
* Added loading of url template tag from future to ensure compatibility with Django < 1.5.
