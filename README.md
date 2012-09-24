# Django Doctor

django-doctor is a Django pluggable app for checking the operational status of 
a Django installation. It includes checking that caching and storage is 
correctly set up, that email is working, etc. 

This is an early draft, so use it at your own risk. 


## Installation

Install `django-doctor` (available on PyPi):

	pip install django-doctor

Add it to `INSTALLED_APPS` in your `settings.py` (so Django can locate template):

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
            <code>'doctor.services.cache.CacheServiceCheck',
'doctor.services.celery.CeleryServiceCheck',
'doctor.services.email.EmailServiceCheck',
'doctor.services.storage.StorageServiceCheck',</code></td>
        <td>Paths to service check classes.</td>
    </tr>
</table>

## Services

We are working on making a pluggable structure for the service check, work in progress. 
Checks for cache and Sentry are currently included by default.


## Tests

Run unit tests by running <code>python setup.py test</code>

