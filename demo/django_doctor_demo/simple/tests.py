# coding=utf8
"""Test suite for django_doctor_demo.homepage application."""
from django.core.urlresolvers import reverse
from django.test import TestCase


class HealthCheckViewTestCase(TestCase):
    """Test health check view."""
    def assertHealthCheck(self, path, status_code=200, runs=1,
                          errors=0, failures=0):
        """Shortcut to test a health check view."""
        url = reverse('simple:health_check', args=[path])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)
        self.assertContains(response, "%d tests run" % runs,
                            status_code=status_code)
        self.assertContains(response, "%d errors" % errors,
                            status_code=status_code)
        self.assertContains(response, "%d failures" % failures,
                            status_code=status_code)

    def test_fake_health_check(self):
        """Fake healthcheck runs (1 success, 1 error, 1 failure)."""
        path = 'django_doctor_demo/simple/healthchecks/FakeHealthCheck'
        self.assertHealthCheck(path, 500, runs=3, errors=1, failures=1)

    def test_fake_success(self):
        """Fake success returns HTTP 200."""
        path = 'django_doctor_demo/simple/healthchecks/FakeHealthCheck/test_success'
        self.assertHealthCheck(path, 200, runs=1, errors=0, failures=0)

    def test_fake_error(self):
        """Fake error returns HTTP 500."""
        path = 'django_doctor_demo/simple/healthchecks/FakeHealthCheck/test_error'
        self.assertHealthCheck(path, 500, runs=1, errors=1, failures=0)

    def test_fake_failure(self):
        """Fake failure returns HTTP 500."""
        path = 'django_doctor_demo/simple/healthchecks/FakeHealthCheck/test_failure'
        self.assertHealthCheck(path, 500, runs=1, errors=0, failures=1)
