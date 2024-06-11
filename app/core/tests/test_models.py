"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """create and return new user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'testpass123'
        name = 'Test User'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalizer(self):
        """Test email is normalized for new users"""
        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_schedule(self):
        """test creating a schedule is successful"""
        user = create_user()
        schedule = models.Schedule.objects.create(user=user, name='Schedule1')
        name = 'Schedule1'
        self.assertEqual(str(schedule), name)

    def test_create_lesson(self):
        """test creating a lesson is successful"""
        user = create_user()
        schedule = models.Schedule.objects.create(user=user)
        lesson = models.Lesson.objects.create(
            user=user,
            name='Lesson1',
            room='Room1',
            start_time='08:00',
            end_time='10:00',
            day='MON'
        )

        schedule.lessons.add(lesson)

        self.assertEqual(str(lesson), lesson.name)
        self.assertEqual(lesson.user, user)
        self.assertEqual(schedule.lessons.first(), lesson)
