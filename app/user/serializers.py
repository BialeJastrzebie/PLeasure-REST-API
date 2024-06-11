"""
Serializers for the user API view
"""
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

from rest_framework import serializers

from friendship.serializers import FriendshipSerializer

from map.serializers import LocationSerializer


class UserSerializer(serializers.ModelSerializer):
    """serializer for the user object"""
    relations = FriendshipSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name',
                  'first_name', 'last_name', 'relations',
                  'favorite_locations', 'coupon_received_locations']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def _get_or_create_relations(self, relations, user):
        auth_user = self.context['request'].user
        for relation in relations:
            relation_obj, create = FriendshipSerializer().get_or_create(
                user=auth_user,
                **relation,
            )
            user.relations.add(relation_obj)

    def _get_or_create_favorite_locations(self, favorite_locations, user):
        auth_user = self.context['request'].user
        for location in favorite_locations:
            location_obj, create = LocationSerializer().get_or_create(
                user=auth_user,
                **location,
            )
            user.favorite_locations.add(location_obj)

    def _get_or_coupon_received_locations(self,
                                          coupon_received_locations,
                                          user):
        auth_user = self.context['request'].user
        for location in coupon_received_locations:
            location_obj, create = LocationSerializer().get_or_create(
                user=auth_user,
                **location,
            )
            user.coupon_received_locations.add(location_obj)

    def create(self, validated_data):
        """create and return a user with encrypted password"""
        relations = validated_data.pop('relations', [])
        favorite_locations = validated_data.pop('favorite_locations', [])
        coupon_received_locations = validated_data.pop(
            'coupon_received_locations', [])
        user = get_user_model().objects.create_user(**validated_data)
        self._get_or_create_relations(relations, user)
        self._get_or_create_favorite_locations(favorite_locations, user)
        self._get_or_coupon_received_locations(coupon_received_locations, user)
        return user

    def update(self, instance, validated_data):
        """updated and return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def delete_favourite_location(self, instance, validated_data):
        """delete a favourite location"""
        location = validated_data.pop('location', None)
        user = super().update(instance, validated_data)
        user.favorite_locations.remove(location)
        return user

    def delete_coupon_received_location(self, instance, validated_data):
        """delete a coupon received location"""
        location = validated_data.pop('location', None)
        user = super().update(instance, validated_data)
        user.coupon_received_locations.remove(location)
        return user


class AuthTokenSerializer(serializers.Serializer):
    """serializer for user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
