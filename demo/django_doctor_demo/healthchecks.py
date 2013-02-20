# -*- coding: utf-8 -*-
"""Health checks."""
import doctor


class FakeHealthCheck(doctor.HealthCheck):
    """Check that health checks are captured."""
    def test_fake_healthcheck(self):
        """Fake healthcheck is captured and passes."""
        self.assertTrue(True)  # Yes, that's a fake healthcheck!
