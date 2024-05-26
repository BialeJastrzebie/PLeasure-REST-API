"""
Tests for the Friendship API
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from friendship.serializers import FriendshipSerializer

from core.models import (
    User,
    Friendship
)

from django.urls import reverse

FRIENDS_URL = '/api/friendship/friends/'


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_friendship(user, friend, is_approved=False):
    return Friendship.objects.create(user=user, friend=friend, is_approved=is_approved)


class FriendshipApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = create_user(email='user1@example.com', password='testpass')
        self.user2 = create_user(email='user2@example.com', password='testpass')
        self.client.force_authenticate(self.user1)

    def test_send_friend_request(self):
        """Test that a user can send a friend request"""
        res = self.client.post(FRIENDS_URL, {'friend': self.user2.id})

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Friendship.objects.count(), 1)
        self.assertEqual(Friendship.objects.get().friend, self.user2)

    def test_view_friends(self):
        """Test that a user can view their friends"""
        create_friendship(self.user1, self.user2, is_approved=True)

        res = self.client.get(FRIENDS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['friend'], self.user2.id)

    def test_create_friend_request(self):
        """Test creating a friend request"""
        url = '/api/friendship/friends/'
        payload = {'friend': self.user2.id}
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Friendship.objects.count(), 1)
        self.assertEqual(Friendship.objects.get().friend, self.user2)

    def test_retrieve_friend_request(self):
        """Test retrieving a friend request"""
        friendship = Friendship.objects.create(user=self.user1, friend=self.user2)
        url = '/api/friendship/friends/' + str(friendship.id) + '/'
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['friend'], self.user2.id)

    def test_update_friend_request(self):
        """Test updating a friend request"""
        friendship = Friendship.objects.create(user=self.user1, friend=self.user2)
        url = '/api/friendship/friends/' + str(friendship.id) + '/'
        payload = {'is_approved': True}
        res = self.client.patch(url, payload)

        friendship.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(friendship.is_approved)

    def test_delete_friend_request(self):
        """Test deleting a friend request"""
        friendship = Friendship.objects.create(user=self.user1, friend=self.user2)
        url = '/api/friendship/friends/' + str(friendship.id) + '/'
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Friendship.objects.filter(id=friendship.id).exists())