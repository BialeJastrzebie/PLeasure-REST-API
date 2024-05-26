from django.urls import path, include

from rest_framework.routers import DefaultRouter

from map.views import LocationViewSet


router = DefaultRouter()
router.register('locations', LocationViewSet, basename='locations')

app_name = 'map'

urlpatterns = [
    path('', include(router.urls)),
]
