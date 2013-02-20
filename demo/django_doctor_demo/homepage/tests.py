# coding=utf8
"""Test suite for django_doctor_demo.homepage application."""
from django.core.urlresolvers import reverse
from django.test import TestCase


class HomepageViewTestCase(TestCase):
    """Test homepage."""
    def test_get(self):
        """Homepage returns HTTP 200."""
        home_url = reverse('homepage:homepage')
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)
