"""
Views for the map app.
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Map, Location, Category, Filter, Coupon
from . import serializers


class BaseViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    """Base viewset for user owned entities"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return self.serializer_class
        return self.serializer_class


class MapViewSet(BaseViewSet):
    """Manage maps in the database"""
    queryset = Map.objects.all()
    serializer_class = serializers.MapSerializer


class LocationViewSet(BaseViewSet):
    """Manage locations in the database"""
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer


class CategoryViewSet(BaseViewSet):
    """Manage categories in the database"""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class FilterViewSet(BaseViewSet):
    """Manage filters in the database"""
    queryset = Filter.objects.all()
    serializer_class = serializers.FilterSerializer


class CouponViewSet(BaseViewSet):
    """Manage coupons in the database"""
    queryset = Coupon.objects.all()
    serializer_class = serializers.CouponSerializer
