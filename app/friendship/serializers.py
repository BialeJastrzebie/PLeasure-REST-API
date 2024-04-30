"""
serializers for friend APIs
"""
from rest_framework import serializers

from core.models import UserFriends


class UserFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFriends
        fields = ['user', 'friend', 'is_approved']
        extra_kwargs = {
            'user': {'write_only': True},
            'friend': {'write_only': True}
        }

    def create(self, validated_data):
        """Create a user friend."""
        user_friend = UserFriends.objects.create(**validated_data)

        return user_friend

    def update(self, instance, validated_data):
        """Update a user friend."""
        instance.is_approved = validated_data.get(
            'is_approved',
            instance.is_approved
            )
        instance.save()

        return instance

    def to_representation(self, instance):
        """Converts the model instance into the desired format."""
        response = super().to_representation(instance)
        response['user'] = instance.user.name
        response['friend'] = instance.friend.name

        return response

    def validate(self, data):
        """Check that the user and friend are not the same."""
        if data['user'] == data['friend']:
            raise serializers.ValidationError(
                "User and friend cannot be the same."
            )

        return data