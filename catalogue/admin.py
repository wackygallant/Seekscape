from django.contrib import admin
from catalogue.models import Trek

# Register your models here.
@admin.register(Trek)
class TrekAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'distance', 'difficulty', 'price',)
    list_filter = ('created_at', 'difficulty', 'duration',)
    search_fields = ('title',)