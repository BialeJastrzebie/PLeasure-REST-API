"""
serializers for plan APIs
"""
from rest_framework import serializers

from core.models import Schedule, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'lesson_name', 'room', 'start_time', 'end_time', 'day']
        read_only_fields = ['id']


class ScheduleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, required=False)

    class Meta:
        model = Schedule
        fields = ['id', 'user',  'lessons']
        read_only_fields = ['id', 'user']

    def _get_or_create_lessons(self, lessons, schedule):
        auth_user = self.context['request'].user
        for lesson in lessons:
            lesson_obj, create = Lesson.objects.get_or_create(
                user=auth_user,
                **lesson,
            )
            schedule.lessons.add(lesson_obj)

    def create(self, validated_data):
        """Create a schedule."""
        lessons = validated_data.pop('lessons')
        schedule = Schedule.objects.create(**validated_data)
        self._get_or_create_lessons(lessons, schedule)
        return schedule
