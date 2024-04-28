from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('schedules', views.ScheduleViewSet)
router.register('lessons', views.LessonViewSet)

app_name = 'plan'

urlpatterns = [
    path('', include(router.urls)),
]
