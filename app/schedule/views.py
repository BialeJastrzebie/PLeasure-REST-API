"""
views for plan
"""

from core.models import Schedule, Lesson
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from . import serializers
from core.views import BaseViewSet


class ScheduleViewSet(BaseViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(Schedule, serializers.ScheduleSerializer,
                         *args, **kwargs)


class LessonViewSet(BaseViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(Lesson, serializers.LessonSerializer,
                         *args, **kwargs)
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
