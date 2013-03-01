from django.conf.urls import patterns, url
from django.views.generic import TemplateView


#: A simple home view.
home = TemplateView.as_view(template_name='homepage.html')


urlpatterns = patterns('', url(r'', home, name='homepage'))
