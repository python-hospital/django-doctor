from django.conf.urls import patterns, url

from doctor.views import HealthCheckView


global_health_check = HealthCheckView.as_view()
local_health_check = HealthCheckView.as_view(
    health_check_root='django_doctor_demo')


urlpatterns = patterns(
    '',
    url(r'^global/(?P<health_check>[A-Za-z0-9/_]+)/?$',
        global_health_check,
        name='global_health_check'),
    url(r'^local/(?P<health_check>[A-Za-z0-9/_]+)/?$',
        local_health_check,
        name='local_health_check'),
)
