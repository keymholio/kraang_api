from django.conf.urls import patterns, include, url
from rest_framework import routers
from talk import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.api_root, name='api-root'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('talk.urls')),
)
