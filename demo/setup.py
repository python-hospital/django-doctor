# coding=utf-8
"""Python packaging for django-doctor's demo project."""
from os.path import dirname, join
from setuptools import setup


NAME = 'django-doctor-demo'
README = open(join(dirname(__file__), 'README')).read().strip()
VERSION = open(join(dirname(dirname(__file__)), 'VERSION')).read().strip()
PACKAGES = ['django_doctor_demo']
REQUIRES = ['django-doctor', 'django-nose']


setup(name=NAME,
      version=VERSION,
      description='Demo project for django-doctor.',
      long_description=README,
      classifiers=['Development Status :: 1 - Planning',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 2.6',
                   'Framework :: Django',
                   ],
      keywords='',
      author='Jon Lønne',
      author_email='jon@funkbit.no',
      url='https://github.com/funkbit/%s' % NAME,
      license='BSD',
      packages=PACKAGES,
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIRES,
      entry_points={
          'console_scripts': [
              'demo = django_doctor_demo.manage:main',
          ]
      },
      )
