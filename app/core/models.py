"""
Database models
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager, PermissionsMixin)


def recipe_image_file_path(instance, filename):
    """generate file path for new plan image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'plan', filename)


def map_image_file_path(instance, filename):
    """generate file path for new map image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'map', filename)


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

    objects = UserManager()

    USERNAME_FIELD = 'email'


class UserFriends(models.Model):
    """User_Friends object"""
    RelationID = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_friends'
    )
    friend = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friend_friends'
    )
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {self.friend.name}"


class Schedule(models.Model):
    """Schedule object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    lessons = models.ManyToManyField('Lesson')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Lesson object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.DateField()

    def __str__(self):
        return self.name


class Map(models.Model):
    """Map object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    id = models.AutoField(primary_key=True)
    locations = models.ManyToManyField('Location', related_name='maps')
    filters = models.ManyToManyField('Filter')

    def __str__(self):
        return self.user.name


class Location(models.Model):
    """Localisation object"""
    map = models.ForeignKey('Map', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    x = models.IntegerField()
    y = models.IntegerField()
    image = models.ImageField(null=True, upload_to=map_image_file_path)
    is_favorite = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Category object"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Filter(models.Model):
    """Filter for filter map object"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Coupon(models.Model):
    """Coupon object"""
    name = models.CharField(max_length=255)
    discount = models.IntegerField()
    location = models.ForeignKey(
        'Location',
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
