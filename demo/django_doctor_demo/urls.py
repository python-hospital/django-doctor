from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    # Health checks.
    url(r'health-check/', include('django_doctor_demo.simple.urls',
                                  app_name='simple', namespace='simple')),
    # Homepage.
    url(r'', include('django_doctor_demo.homepage.urls',
                     app_name='homepage', namespace='homepage'))
)
