from django.urls import path, include

from rest_framework.routers import DefaultRouter

from schedule.views import ScheduleViewSet, LessonViewSet

router = DefaultRouter()
router.register('schedules', ScheduleViewSet, basename='schedules')
router.register('lessons', LessonViewSet, basename='lessons')


app_name = 'schedule'

urlpatterns = [
    path('', include(router.urls)),
]
