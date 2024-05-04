"""
Tests for the Schedule API
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Map,
    Location,
    Category,
    Filter,
    Coupon
)

from map.serializers import MapSerializer

MAP_URL = reverse('map:map-list')


def create_user(**params):
    defaults = {
        'email': 'user@example.com',
        'password': 'testpass',
        'name': 'Test user'
    }
    defaults.update(params)

    return get_user_model().objects.create_user(**defaults)


def create_category(user, **params):
    """Create and return a sample category"""
    defaults = {
        'name': 'Sample category',
    }
    defaults.update(params)

    return Category.objects.create(user=user, **defaults)


def create_coupon(user, **params):
    """Create and return a sample coupon"""
    defaults = {
        'name': 'Sample coupon',
        'valid_until': '12:45',
        'is_active': True,
    }
    defaults.update(params)

    return Coupon.objects.create(user=user, **defaults)


def create_filter(user, **params):
    """Create and return a sample filter"""
    defaults = {
        'name': 'Sample filter',
        'is_active': True,
    }
    defaults.update(params)

    return Filter.objects.create(user=user, **defaults)


def create_location(user, **params):
    """Create and return a sample location"""
    defaults = {
        'name': 'Sample location',
        'address': 'Sample address',
        'x': 0.123,
        'y': 2.123,
        'image': None,
        'is_favorite': False,
        'categories': create_category(user),
        'coupons': create_coupon(user),
    }
    defaults.update(params)

    return Location.objects.create(user=user, **defaults)


def create_map(user, **params):
    """Create and return a sample map"""
    map = Map.objects.create(user=user, **params)
    map.locations.add(create_location(user))
    map.filters.add(create_filter(user))

    return map


class PrivateMapApiTests(TestCase):
    """Test authenticated map API access"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_maps(self):
        """Test retrieving a list of maps"""
        create_map(user=self.user)
        create_map(email='testXD@example.com')

        res = self.client.get(MAP_URL)

        maps = Map.objects.all().order_by('-id')
        serializer = MapSerializer(maps, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_maps_limited_to_user(self):
        """Test retrieving maps for user"""
        user2 = create_user(email='testXD@example.com')
        create_map(user=user2)
        create_map(user=self.user)

        res = self.client.get(MAP_URL)

        maps = Map.objects.filter(user=self.user)
        serializer = MapSerializer(maps, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_create_map_successful(self):
        """Test creating a new map"""
        payload = {'user': self.user}

        self.client.post(MAP_URL, payload)

        exists = Map.objects.filter(
            user=self.user
        ).exists()

        self.assertTrue(exists)

    def test_create_map_invalid(self):
        """Test creating a new map with invalid payload"""
        payload = {'user': ''}

        res = self.client.post(MAP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PublicMapApiTests(TestCase):
    """Test unauthenticated map API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(MAP_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
