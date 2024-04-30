"""
Tests for the lesson API
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Lesson

from schedule.serializers import LessonSerializer

LESSON_URL = reverse('schedule:lesson-list')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_lesson(user, **params):
    """Create and return a sample lesson"""
    defaults = {
        'name': 'Lesson1',
        'room': 'Room1',
        'start_time': '9:15',
        'end_time': '10:15',
        'day': '2024-04-04',
    }
    defaults.update(params)

    return Lesson.objects.create(user=user, **defaults)


class PublicScheduleAPITest(TestCase):
    """Test unauthenticated schedule API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(LESSON_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateScheduleAPITest(TestCase):
    """Test authenticated schedule API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_lesssons(self):
        """Test retrieving a list of lessons"""
        create_lesson(user=self.user)
        create_lesson(user=self.user)

        res = self.client.get(LESSON_URL)

        lessons = Lesson.objects.all().order_by('id')
        serializer = LessonSerializer(lessons, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_lessons_limited_to_user(self):
        """Test that lessons for the authenticated user are returned"""
        user2 = create_user(email='other@example.com', password='test123')
        create_lesson(user=user2)
        create_lesson(user=self.user)

        res = self.client.get(LESSON_URL)
        lessons = Lesson.objects.filter(user=self.user)
        serializer = LessonSerializer(lessons, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_create_lesson_successful(self):
        """Test creating a new lesson"""
        payload = {
            'name': 'Lesson1',
            'room': 'Room1',
            'start_time': '9:15',
            'end_time': '10:15',
            'day': '2024-04-04',
        }
        self.client.post(LESSON_URL, payload)

        exists = Lesson.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_lesson_invalid(self):
        """Test creating a new lesson with invalid payload"""
        payload = {
            'name': '',
            'room': 'Room1',
            'start_time': '9:15',
            'end_time': '10:15',
            'day': '2024-04-04',
        }
        res = self.client.post(LESSON_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_lesson(self):
        """Test deleting a lesson"""
        lesson = create_lesson(user=self.user)

        res = self.client.delete(
            reverse('schedule:lesson-detail', args=[lesson.id])
        )

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=lesson.id).exists())
