# Django Doctor

django-doctor is a Django pluggable application for checking the operational 
status of a Django installation. It includes checking that caching and storage 
is correctly set up, that email is working, etc. 

This is an early draft, so use it at your own risk.


## Installation

Install `django-doctor` (available on PyPi):

	pip install django-doctor

Add it to `INSTALLED_APPS` in your `settings.py` (so Django can locate 
templates):

	INSTALLED_APPS += ['doctor']

And add it to your root URLconf:
    
    urlpatterns = patterns('',
	   url(r'^doctor/', include('doctor.urls')),
       ...
    )


## Settings

These are the available configurable settings, along with their default values:

<table>
    <tr>
        <th align="left">Name</th>
        <th align="left">Default</th>
        <th align="left">Description</th>
    </tr>
    <tr>
        <td><code>DOCTOR_BASE_TEMPLATE</code></td>
        <td><code>'base.html'</code></td>
        <td>The template all the doctor templates should inherit from</td>
    </tr>
    <tr>
        <td><code>DOCTOR_SERVICES</code></td>
        <td>
            <code>'doctor.services.cache.CacheServiceCheck',<br>
'doctor.services.celery_check.CeleryServiceCheck',<br>
'doctor.services.email.EmailServiceCheck',<br>
'doctor.services.storage.StorageServiceCheck',</code></td>
        <td>Paths to service check classes.</td>
    </tr>
    <tr>
        <td><code>DOCTOR_STORAGE_CLASSES</code></td>
        <td>
            <code>settings.DEFAULT_FILE_STORAGE,<br>
settings.STATICFILES_STORAGE,</code></td>
        <td>Paths to storage classes to check.</td>
    </tr>
</table>

## Services

We are working on making a pluggable structure for the service check, work in 
progress. Checks for cache, Celery, email and storages are currently included 
by default.


## Tests

Run unit tests by running <code>python setup.py test</code>


## TODO

* Set up the project tests so they can run standalone
* Refine the service class approach
* Include sending of test email in a view?
* Implement more health checks:
    * Databases
    * Haystack?
    * Sentry?
    * That the request.is_secure() check is properly set up
