"""
views for plan
"""

from core.models import Schedule, Lesson
from . import serializers
from core.views import BaseViewSet


class ScheduleViewSet(BaseViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(Schedule, serializers.ScheduleSerializer,
                         *args, **kwargs)


class LessonViewSet(BaseViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(Lesson, serializers.LessonSerializer,
                         *args, **kwargs)
