"""Django settings for django-doctor demo project."""
from os.path import abspath, dirname, join


# Configure some relative directories.
django_doctor_demo_dir = dirname(abspath(__file__))
demo_dir = dirname(django_doctor_demo_dir)
root_dir = dirname(demo_dir)
data_dir = join(root_dir, 'var')


# Mandatory settings.
ROOT_URLCONF = 'django_doctor_demo.urls'
WSGI_APPLICATION = 'django_doctor_demo.wsgi.application'


# Database.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(data_dir, 'db.sqlite'),
    }
}


# Media and static files.
MEDIA_ROOT = join(data_dir, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = join(data_dir, 'static')
STATIC_URL = '/static/'


# Applications.
INSTALLED_APPS = (
    # Standard Django applications.
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # The actual django-doctor demo.
    'django_doctor_demo.homepage',
    # This demo project is part of django-doctor test suite.
    'django_nose',
)


# Default middlewares. You may alter the list later.
MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]


# Development configuration.
DEBUG = True
TEMPLATE_DEBUG = DEBUG
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--verbose',
             '--nocapture',
             '--rednose',
             '--with-id',  # allows --failed which only reruns failed tests
             '--id-file=%s' % join(data_dir, 'test', 'noseids'),
             '--with-doctest',
             '--with-xunit',
             '--xunit-file=%s' % join(data_dir, 'test', 'nosetests.xml'),
             '--with-coverage',
             '--cover-erase',
             '--cover-package=doctor',
             '--cover-package=django_doctor_demo',
             '--no-path-adjustment',
             '--all-modules',
             '--attr=!is_healthcheck',
             ]
