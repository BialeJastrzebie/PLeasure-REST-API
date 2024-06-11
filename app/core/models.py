"""
Database models
"""
import uuid

from django.conf import settings
from django.db import models
import os
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager, PermissionsMixin)


def location_image_file_path(instance, filename):
    """generate file path for new location image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'location', filename)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_field):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    relations = models.ManyToManyField('Friendship', related_name='relations')
    favorite_locations = models.ManyToManyField('Location', blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'


class Friendship(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendship_requests_sent'
    )
    friend = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendship_requests_received'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'friend')

    def approve(self):
        self.is_approved = True
        self.save()

    def __str__(self):
        return f"{self.user} - {self.friend}"


class Schedule(models.Model):
    """Schedule object"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    lessons = models.ManyToManyField('Lesson')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Lesson object"""
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)

    def __str__(self):
        return self.name


class Location(models.Model):
    """Location object"""
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=40)
    description = models.TextField(blank=False, max_length=400)
    image = models.ImageField(null=True, upload_to=location_image_file_path)
    url = models.URLField(max_length=255, verbose_name='URL')
    coupon = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.name
