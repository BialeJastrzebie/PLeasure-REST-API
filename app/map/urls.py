from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('maps', views.MapViewSet)
router.register('locations', views.LocationViewSet)
router.register('categories', views.CategoryViewSet)
router.register('filters', views.FilterViewSet)
router.register('coupons', views.CouponViewSet)


app_name = 'map'

urlpatterns = [
    path('', include(router.urls)),
]
