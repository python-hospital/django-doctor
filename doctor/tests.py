from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class DoctorAuthorizationTests(TestCase):

    def setUp(self):

        # Create active user to test with
        user = User(username='example_user', is_active=True)
        user.set_password('1234')
        user.save()

        self.user = user

    def testAnonymous(self):

        # Health check is IP address filtered
        response = self.client.get(reverse('doctor-health-check'))

        if '127.0.0.1' in settings.INTERNAL_IPS:
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response['Content-Type'], 'text/plain')
        else:
            self.assertEquals(response.status_code, 404)

        # Check non-accessable pages
        response = self.client.get(reverse('doctor-index'))
        self.assertEquals(response.status_code, 404)

        response = self.client.get(reverse('doctor-technical'))
        self.assertEquals(response.status_code, 404)

        response = self.client.get(reverse('doctor-server-error'))
        self.assertEquals(response.status_code, 404)

    def testNonPrivileged(self):

        # Sign in user
        self.client.login(username=self.user.username, password='1234')

        # Health check is IP address filtered
        response = self.client.get(reverse('doctor-health-check'))

        if '127.0.0.1' in settings.INTERNAL_IPS:
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response['Content-Type'], 'text/plain')
        else:
            self.assertEquals(response.status_code, 404)

        # Check non-accessable pages
        response = self.client.get(reverse('doctor-index'))
        self.assertEquals(response.status_code, 404)

        response = self.client.get(reverse('doctor-technical'))
        self.assertEquals(response.status_code, 404)

        response = self.client.get(reverse('doctor-server-error'))
        self.assertEquals(response.status_code, 404)


class DoctorViewTests(TestCase):

    def setUp(self):

        # Create super user to test with
        user = User(username='example_user', is_active=True, is_superuser=True)
        user.set_password('1234')
        user.save()

        self.user = user

    def testPrivileged(self):

        # Sign in user
        self.client.login(username=self.user.username, password='1234')

        # Check pages
        response = self.client.get(reverse('doctor-index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/index.html')

        response = self.client.get(reverse('doctor-health-check'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Type'], 'text/plain')

        response = self.client.get(reverse('doctor-technical'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/technical_info.html')

    def testForceServerError(self):
        
        # Make superuser
        self.user.is_superuser = True
        self.user.save()

        # Sign in user
        self.client.login(username=self.user.username, password='1234')

        with self.assertRaises(Exception):
            response = self.client.get(reverse('doctor-server-error'))
