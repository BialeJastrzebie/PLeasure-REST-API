from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Schedule

# from schedule.serializers import ScheduleSerializer

SCHEDULES_URL = reverse('schedule:schedule-list')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_schedule(user, **params):
    lesson = {
        'lessons': 'Lesson1',
    }
    lesson.update(params)
    schedule = Schedule.objects.create(user=user, **lesson)
    schedule.lessons.set(lesson)

    return schedule


class PublicScheduleAPITest(TestCase):
    """Test unauthenticated schedule API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(SCHEDULES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateScheduleAPITest(TestCase):
    """Test authenticated schedule API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    # def test_retrieve_schedules(self):
    #     """Test retrieving a list of schedules"""
    #     create_schedule(user=self.user)
    #     create_schedule(user=self.user)

    #     res = self.client.get(SCHEDULES_URL)

    #     schedules = Schedule.objects.all().order_by('-id')
    #     serializer = ScheduleSerializer(schedules, many=True)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)

    # def test_schedules_limited_to_user(self):
    #     """Test that schedules for the authenticated user are returned"""
    #     user2 = create_user(email='other@example.com', password='test123')
    #     create_schedule(user=user2)
    #     create_schedule(user=self.user)

    #     res = self.client.get(SCHEDULES_URL)

    #     schedules = Schedule.objects.filter(user=self.user)
    #     serializer = ScheduleSerializer(schedules, many=True)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data, serializer.data)

    # def test_create_schedule(self):
    #     """Test creating a new schedule"""
    #     payload = {'lessons': 'Lesson2'}
    #     res = self.client.post(SCHEDULES_URL, payload)

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     schedule = Schedule.objects.get(id=res.data['id'])
    #     self.assertEqual(schedule.lessons, payload['lessons'])
    #     self.assertEqual(schedule.user, self.user)

    # def test_update_schedule(self):
    #     """Test updating a schedule"""
    #     schedule = create_schedule(user=self.user)
    #     lesson = Lesson.objects.create(name='Lesson3') 
    #     payload = {'lessons': [lesson.id]}  

    #     url = reverse('schedule:schedule-detail', args=[schedule.id])
    #     res = self.client.patch(url, payload, format='json')

    #     schedule.refresh_from_db()
    #     self.assertEqual(schedule.lessons.first().id, payload['lessons'][0])

    # def test_delete_schedule(self):
    #     """Test deleting a schedule"""
    #     schedule = create_schedule(user=self.user)

    #     url = reverse('schedule:schedule-detail', args=[schedule.id])
    #     res = self.client.delete(url)

    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Schedule.objects.filter(id=schedule.id).exists())
