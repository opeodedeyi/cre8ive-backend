from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile, Skill, FollowLog


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser',
            'groups', 
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'name', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'name', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'name',)
    ordering = ('email', 'name',)
    filter_horizontal = ('groups', 'user_permissions',)


class ProfileAdmin(admin.ModelAdmin):
    fields = ('user.name',)


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(FollowLog)