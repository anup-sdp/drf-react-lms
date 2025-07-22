# fix by: kimi k2
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Columns shown on the user list page
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    ordering  = ('username',)

    # Re-use stock fieldsets and add the extra fields
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra info', {'fields': ('role', 'mobile_no')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'mobile_no')}),
    )