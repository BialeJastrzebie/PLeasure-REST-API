from rest_framework import serializers

from core.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'category', 'address', 'latitude', 'longitude',
                  'description', 'url', 'coupon', 'image']
        read_only_fields = ['id']

    def get_or_create(self, user, param):
        location, created = Location.objects.get_or_create(user=user, **param)

        return location
