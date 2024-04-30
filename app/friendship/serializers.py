"""
serializers for friend APIs
"""
from rest_framework import serializers

from core.models import UserFriends


class UserFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFriends
        fields = ['RelationID', 'user_email', 'friend_email', 'is_approved']
        read_only_fields = ['RelationID']

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
