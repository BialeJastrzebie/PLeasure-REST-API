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


def create_map(user, **params):
    """Create and return a sample map"""
    pass
