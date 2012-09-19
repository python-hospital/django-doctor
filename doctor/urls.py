from django.conf.urls import patterns, include, url

urlpatterns = patterns('doctor.views',

	url(r'^health-check/$', 'health_check', name='doctor-health-check'),
	url(r'^technical/$', 'technical_info', name='doctor-technical'),
	url(r'^server-error/$', 'force_server_error', name='doctor-server-error'),
	
    url(r'^$', 'index', name='doctor-index'),

)
