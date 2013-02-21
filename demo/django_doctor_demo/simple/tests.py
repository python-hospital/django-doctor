# coding=utf8
"""Test suite for django_doctor_demo.homepage application."""
from django.core.urlresolvers import reverse
from django.test import TestCase


class GlobalHealthCheckViewTestCase(TestCase):
    """Test global (no root) health check view."""
    def setUp(self):
        super(GlobalHealthCheckViewTestCase, self).setUp()
        self.url_name = 'simple:global_health_check'
        self.root = 'django_doctor_demo/'

    def assertHealthCheck(self, path, status_code=200, runs=1, errors=0,
                          failures=0):
        """Shortcut to test a health check view.

        Gets the health-check view at ``path``.
        Checks status code and displayed number of tests run, errors and
        failures.

        """
        path = '{}{}'.format(self.root, path)
        url = reverse(self.url_name, args=[path])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)
        self.assertContains(response, "%d tests run" % runs,
                            status_code=status_code)
        self.assertContains(response, "%d errors" % errors,
                            status_code=status_code)
        self.assertContains(response, "%d failures" % failures,
                            status_code=status_code)

    def test_fake_module(self):
        """Module-level health-check runs (1 success, 1 error, 1 failure)."""
        path = 'simple/healthchecks'
        self.assertHealthCheck(path, 500, runs=3, errors=1, failures=1)

    def test_fake_class(self):
        """Class-level health-check runs (1 success, 1 error, 1 failure)."""
        path = 'simple/healthchecks/FakeHealthCheck'
        self.assertHealthCheck(path, 500, runs=3, errors=1, failures=1)

    def test_fake_success(self):
        """Fake success (method-level) returns HTTP 200."""
        path = 'simple/healthchecks/FakeHealthCheck/test_success'
        self.assertHealthCheck(path, 200, runs=1, errors=0, failures=0)

    def test_fake_error(self):
        """Fake error returns HTTP 500."""
        path = 'simple/healthchecks/FakeHealthCheck/test_error'
        self.assertHealthCheck(path, 500, runs=1, errors=1, failures=0)

    def test_fake_failure(self):
        """Fake failure returns HTTP 500."""
        path = 'simple/healthchecks/FakeHealthCheck/test_failure'
        self.assertHealthCheck(path, 500, runs=1, errors=0, failures=1)


class LocalHealthCheckViewTestCase(GlobalHealthCheckViewTestCase):
    """Test local (with root) health check view.

    The test suite is the same, we just adapt the :py:meth:`setUp`
    method to make it local, i.e. change URL and prefix URLs without root.

    """
    def setUp(self):
        super(LocalHealthCheckViewTestCase, self).setUp()
        self.url_name = 'simple:local_health_check'
        self.root = ''
