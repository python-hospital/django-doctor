from django.conf.urls import url

from doctor import views


urlpatterns = [

    url(r'^health-check/$', views.health_check, name='doctor-health-check'),
    url(r'^technical/$', views.technical_info, name='doctor-technical'),
    url(r'^server-error/$', views.force_server_error, name='doctor-server-error'),

    url(r'^$', views.index, name='doctor-index'),

]
