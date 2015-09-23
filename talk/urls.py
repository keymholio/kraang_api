from django.conf.urls import patterns, url
from talk import views

urlpatterns = patterns('',
    url(r'^translate/$', views.Translate.as_view(), name='translate'),
    url(r'^hipchat/$', views.Hipchat.as_view(), name='hipchat'),
)
