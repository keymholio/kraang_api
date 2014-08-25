from django.conf.urls import patterns, url, include
from rest_framework import routers
from talk import views

router = routers.DefaultRouter()
router.register(r'sentences', views.SentenceViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
