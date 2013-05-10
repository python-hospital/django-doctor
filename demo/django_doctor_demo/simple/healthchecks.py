# -*- coding: utf-8 -*-
"""Health checks."""
from hospital import HealthCheck


class FakeHealthCheck(HealthCheck):
    """Check that health checks are captured."""
    def test_success(self):
        """Successful healthcheck is captured and passes."""
        self.assertTrue(True)  # Yes, that's a fake healthcheck!

    def test_failure(self):
        """Failing healthcheck is captured and reports failure."""
        self.assertTrue(False, 'This failure is here by design!')

    def test_error(self):
        """Errorneous healthcheck is captured and reports error."""
        data = {}
        self.assertTrue(data['unavailable'], 'This error is here by design!')
