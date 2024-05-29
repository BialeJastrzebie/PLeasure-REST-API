"""
views for map
"""

from core.models import Location
from . import serializers
from core.views import BaseViewSet


class LocationViewSet(BaseViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(Location, serializers.LocationSerializer,
                         *args, **kwargs)

    def get_queryset(self):
        """Return all objects"""
        return self.queryset.all()
