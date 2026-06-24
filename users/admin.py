from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from users.models import CustomUser, GroupProxy

# Unregister the original Group
admin.site.unregister(Group)

# Register the proxy instead
@admin.register(GroupProxy)
class GroupProxyAdmin(GroupAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser',)
    list_filter = ('is_staff', 'is_active', 'is_superuser',)
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('date_joined',)
