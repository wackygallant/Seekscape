from django.contrib import admin
from unfold.admin import ModelAdmin

from operations.models import Trip, Booking, Participants

# Register your models here.
@admin.register(Trip)
class TripAdmin(ModelAdmin):
    list_display = ('trip_code', 'start_date', 'end_date', 'remaining_slots', 'booking_deadline',)
    list_filter = ('start_date', 'end_date', 'trip_code', 'is_active')

@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ('trip', 'number_of_pax', 'status', 'total_price',)
    list_filter = ('trip', 'status',)

@admin.register(Participants)
class ParticipantsAdmin(ModelAdmin):
    list_display = ('booking', 'first_name', 'last_name', 'email', 'phone', 'created_at',)
    list_filter = ('booking', 'created_at')