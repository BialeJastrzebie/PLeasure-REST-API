"""
views for Schedules
"""
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import User, Schedule, Lesson
from . import serializers


class ScheduleViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    """Manage schedules in the database"""
    authentication_classes = TokenAuthentication
    permission_classes = IsAuthenticated
    queryset = Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new schedule"""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.ScheduleSerializer
        return self.serializer_class



class LessonViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    """Manage lessons in the database"""
    authentication_classes = TokenAuthentication
    permission_classes = IsAuthenticated
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(schedule__user=self.request.user)

    def perform_create(self, serializer):
        """Create a new lesson"""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.LessonSerializer
        return self.serializer_class

