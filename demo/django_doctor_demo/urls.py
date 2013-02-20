from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


home = TemplateView.as_view(template_name='home.html')


urlpatterns = patterns(
    '',
    # Homepage.
    url(r'', include('django_doctor_demo.homepage.urls',
                     app_name='homepage', namespace='homepage'))
)
