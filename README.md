# django-doctor

django-doctor is a Django app for checking the operational status of a Django 
installation. It includes checking that caching and storage is correctly 
set up, that email is working, etc. 

This is an early draft, so use it at your own risk. 


## Installation

Install `django-doctor` (available on PyPi):

	pip install django-doctor

Add it to `INSTALLED_APPS` in your `settings.py`:

	INSTALLED_APPS += ['doctor']

And add it to your root urls.py file:

	url(r'^doctor/', include('doctor.urls')),


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
</table>

## Tests

Run unit tests by running <code>python setup.py test</code>

