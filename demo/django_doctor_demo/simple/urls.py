from django.conf.urls import patterns, url

from doctor.views import HealthCheckView


health_check = HealthCheckView.as_view()


urlpatterns = patterns(
    '',
    # Health checks.
    url(r'^(?P<health_check>[A-Za-z0-9/_]+)/?$',
        health_check,
        name='health_check'),
)
