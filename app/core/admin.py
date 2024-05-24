"""
Django admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from leaflet.admin import LeafletGeoAdmin

from . import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
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
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


class MapAdmin(LeafletGeoAdmin):
    list_display = ['name', 'address', 'location', 'image',
                    'categories', 'coupons']
    search_fields = ['name', 'address', 'categories', 'coupons']
    ordering = ['name']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.UserFriends)
admin.site.register(models.Schedule)
admin.site.register(models.Lesson)
# admin.site.register(models.Map, MapAdmin)
