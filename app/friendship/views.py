"""
Views for friend
"""


from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import UserFriends
from . import serializers


class UserFriendsViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    """Manage friends in the database"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserFriends.objects.all()
    serializer_class = serializers.UserFriendsSerializer

    def get_queryset(self):
        """Return objects for the current user"""
        return UserFriends.objects.filter(user_email=self.request.user.email)

    def perform_create(self, serializer):
        """Create a new user friend"""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.UserFriendsSerializer
        return self.serializer_class
