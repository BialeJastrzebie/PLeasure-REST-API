"""
serializers for Schedules APIs
"""
from rest_framework import serializers

from core.models import User, Schedule, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """for tags"""
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'room', 'start_time', 'end_time', 'day']
        read_only_fields = ['id']


class ScheduleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, required=False)

    class Meta:
        model = Schedule
        fields = ['id', 'user', 'name', 'lessons']
        ready_only_fields = ['id']
