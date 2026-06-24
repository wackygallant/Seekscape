from django.contrib import admin
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE
from tinymce.models import HTMLField

from catalogue.models import Trek


# Register your models here.
@admin.register(Trek)
class TrekAdmin(ModelAdmin):
    list_display = ('title', 'duration', 'distance', 'difficulty', 'price',)
    list_filter = ('created_at', 'difficulty', 'duration',)
    search_fields = ('title',)

    formfield_overrides = {
        # This tells Unfold's admin to use TinyMCE widget for HTMLField
        HTMLField: {'widget': TinyMCE()},
    }
