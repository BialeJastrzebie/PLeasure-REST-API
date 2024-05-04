"""
Tests for the Friendship API
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from friendship.serializers import UserFriendsSerializer

from core.models import (
    User,
    UserFriends
)


FRIENDS_URL = '/api/friendship/friends/'


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_friend(user, **params):
    """Create and return a sample friend"""
    defaults = {
        'user_email': 'user@example.com',
        'friend_email': 'admin@admin.com',
        'is_approved': False,
    }
    defaults.update(params)

    return UserFriends.objects.create(user=user, **defaults)


class PublicFriendshipAPITest(TestCase):
    """Test unauthenticated friendship API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(FRIENDS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFriendshipAPITest(TestCase):
    """Test authenticated friendship API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_friends(self):
        """Test retrieving friends"""
        create_friend(user=self.user)

        res = self.client.get(FRIENDS_URL)

        friends = UserFriends.objects.all()
        serializer = UserFriendsSerializer(friends, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_friend_successful(self):
        """Test creating a new friend"""
        user2 = User.objects.create_user(
            email='friend@example.com',
            password='testpass123'
        )
        payload = {
            'user_email': self.user.email,
            'friend_email': user2.email,
            'is_approved': False,
        }
        res = self.client.post(FRIENDS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        friend = UserFriends.objects.get(RelationID=res.data['RelationID'])
        self.assertEqual(friend.user_email, payload['user_email'])

    def test_update_friend(self):
        """Test updating a friend"""
        friend = create_friend(user=self.user)
        payload = {
            'is_approved': True
        }
        url = '/api/friendship/friends/' + str(friend.RelationID) + '/'
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        friend.refresh_from_db()
        self.assertTrue(friend.is_approved)

    def test_delete_friend(self):
        """Test deleting a friend"""
        friend = create_friend(user=self.user)
        url = '/api/friendship/friends/' + str(friend.RelationID) + '/'
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserFriends.objects.count(), 0)
