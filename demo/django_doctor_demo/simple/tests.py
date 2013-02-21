# coding=utf8
"""Test suite for django_doctor_demo.homepage application."""
from django.core.urlresolvers import reverse
from django.test import TestCase


class HealthCheckViewTestCase(TestCase):
    """Test health check view."""
    def test_fake_health_check(self):
        """Fake healthcheck runs health checks (1 success, 1 error, 1 failure).

        """
        url = reverse('simple:health_check',
                      args=['django_doctor_demo/simple/healthchecks/FakeHealthCheck'])
        response = self.client.get(url)
        status_code = 500
        self.assertEqual(response.status_code, status_code)
        self.assertContains(response, "3 tests run", status_code=status_code)
        self.assertContains(response, "1 errors", status_code=status_code)
        self.assertContains(response, "1 failures", status_code=status_code)

    def test_fake_success(self):
        """Fake success returns HTTP 200."""
        url = reverse('simple:health_check',
                      args=['django_doctor_demo/simple/healthchecks/FakeHealthCheck/test_success'])
        response = self.client.get(url)
        status_code = 200
        self.assertEqual(response.status_code, status_code)
        self.assertContains(response, "1 tests run", status_code=status_code)
        self.assertContains(response, "0 errors", status_code=status_code)
        self.assertContains(response, "0 failures", status_code=status_code)

    def test_fake_error(self):
        """Fake error returns HTTP 500."""
        url = reverse('simple:health_check',
                      args=['django_doctor_demo/simple/healthchecks/FakeHealthCheck/test_error'])
        response = self.client.get(url)
        status_code = 500
        self.assertEqual(response.status_code, status_code)
        self.assertContains(response, "1 tests run", status_code=status_code)
        self.assertContains(response, "1 errors", status_code=status_code)
        self.assertContains(response, "0 failures", status_code=status_code)

    def test_fake_failure(self):
        """Fake failure returns HTTP 500."""
        url = reverse('simple:health_check',
                      args=['django_doctor_demo/simple/healthchecks/FakeHealthCheck/test_failure'])
        response = self.client.get(url)
        status_code = 500
        self.assertEqual(response.status_code, status_code)
        self.assertContains(response, "1 tests run", status_code=status_code)
        self.assertContains(response, "0 errors", status_code=status_code)
        self.assertContains(response, "1 failures", status_code=status_code)
