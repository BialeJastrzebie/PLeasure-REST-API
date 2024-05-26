"""
serializers for friend APIs
"""
from rest_framework import serializers

from core.models import Friendship


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ['user', 'friend', 'created_at', 'is_approved']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        """Create a user friend."""
        friendship = Friendship.objects.create(**validated_data)

        return friendship

    def update(self, instance, validated_data):
        """Update a user friend."""
        instance.is_approved = validated_data.get(
            'is_approved',
            instance.is_approved
            )
        instance.save()

        return instance
