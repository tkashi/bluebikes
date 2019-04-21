from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import StationViewSet, TripViewSet

router = DefaultRouter()
router.register(r'stations', StationViewSet)
router.register(r'trips', TripViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]