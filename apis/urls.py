from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'stations', views.StationViewSet)
router.register(r'trips', views.TripViewSet)
router.register(r'tripsummary', views.TripSummaryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]