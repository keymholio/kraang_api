from django.conf.urls import patterns, url, include
from talk import views
from rest_framework import routers

#router = routers.DefaultRouter()
#router.register(r'translate', 'translate', views.Translate)

urlpatterns = patterns('',
    url(r'^translate/$', views.Translate.as_view(), name='translate'),
)
