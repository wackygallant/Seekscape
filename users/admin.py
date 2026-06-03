from django.contrib import admin
from users.models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser',)
    list_filter = ('is_staff', 'is_active', 'is_superuser',)
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('date_joined',)
