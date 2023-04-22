from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (Comment, Director, FriendRequest, Movie, Post, User,
                     UserProfile)


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = ((None, {'fields': ('email', 'password')}),
                 (
        ('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }
    ),
        (('Important dates'), {
            'fields': (
                'last_login',
            )
        }
    ),
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
                'is_superuser'
            )
        }),
    )


admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(FriendRequest)
