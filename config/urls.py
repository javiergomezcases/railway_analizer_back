from django.conf.urls import include, url
from rest_framework import routers

from app.base_data import views as bd_views

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'base-data/tracing', bd_views.TracingViewSet, basename="bd_tracing")

urlpatterns = [
    url(r'^', include(router.urls)),
]
