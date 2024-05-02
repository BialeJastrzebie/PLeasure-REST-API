from rest_framework import serializers

from core.models import Map, Location, Category, Filter, Coupon


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = ['id', 'name', 'is_active']
        read_only_fields = ['id']


class LocationSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, required=False)

    class Meta:
        model = Location
        fields = ['id', 'name', 'x', 'y', 'image',
                  'is_favorite', 'categories', 'coupons']
        read_only_fields = ['id']


class MapSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, required=False)
    filters = FilterSerializer(many=True, required=False)

    class Meta:
        model = Map
        fields = ['id', 'locations', 'filters']
        read_only_fields = ['id']


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'name', 'valid_until', 'is_active']
        read_only_fields = ['id']
