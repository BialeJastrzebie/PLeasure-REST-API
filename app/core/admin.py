"""
Django admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'favorite_locations', 'coupon_received_locations')}), # noqa
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )
    filter_horizontal = ('favorite_locations', 'coupon_received_locations')


class LocationAdmin(admin.ModelAdmin):
    """Define the admin pages for locations"""
    ordering = ['id']
    list_display = ['name', 'category', 'address']
    fieldsets = (
        (None, {'fields': ('name', 'category', 'address',
                           'latitude', 'longitude')}),
        (
            _('Details'),
            {
                'fields': (
                    'description',
                    'url',
                    'coupon',
                    'image',
                )
            }
        ),
    )
    readonly_fields = ['id']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Friendship)
admin.site.register(models.Schedule)
admin.site.register(models.Lesson)
admin.site.register(models.Location, LocationAdmin)
