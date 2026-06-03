from django.db import models
from django.conf import settings
from catalogue.models import Trek
from utils.models import BaseModel
from utils.custom_utils import generate_trip_id, generate_booking_id

class Trip(BaseModel):
    trek = models.ForeignKey(Trek, on_delete=models.CASCADE, related_name='trips')

    trip_code = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        unique=True,
        help_text="Format: Trek-YYYYMMDD-NNNN"
    )
    
    start_date = models.DateField()
    end_date = models.DateField()
    max_occupancy = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    booking_deadline = models.DateField(null=True, blank=True)

    @property
    def remaining_slots(self):
        return self.max_occupancy - self.bookings.count()

    @property
    def is_booking_open(self):
        from django.utils import timezone

        if not self.is_active:
            return False

        if self.booking_deadline and timezone.now().date() > self.booking_deadline:
            return False

        if self.remaining_slots <= 0:
            return False

        return True
    
    def save(self, *args, **kwargs):
        '''
        Overriding the save method to generate a custom ID if not provided.
        '''
        if not self.trip_code:
            self.trip_code = generate_trip_id(self)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.trip_code} - ({self.trek.title}) - ({self.trek.duration} days)"
    
    class Meta:
        verbose_name = 'Trip'
        verbose_name_plural = 'Trips'
        db_table = 'trips'
        ordering = ['-start_date'] # Order by start date


class Booking(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')
    number_of_pax = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_code = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.total_price = self.number_of_pax * self.trip.trek.price

        if not self.trip_code:
            # Loop until we find a code that isn't in the database yet
            is_unique = False
            while not is_unique:
                candidate_code = generate_booking_id()
                if not Booking.objects.filter(trip_code=candidate_code).exists():
                    self.trip_code = candidate_code
                    is_unique = True
        
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trip} - {self.number_of_pax} - {self.trip.trip_code}"
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        db_table = 'bookings'
        ordering = ['-created_at']

class Participants(BaseModel):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Prefer not to say'),
    ]

    booking = models.ForeignKey(
        'Booking', 
        on_delete=models.CASCADE, 
        related_name='participants'
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    phone = models.CharField(max_length=10)
    emergency_contact = models.CharField(max_length=10, blank=True, null=True)
    medical_condition = models.BooleanField(default=False)
    medical_condition_details = models.TextField(blank=True, null=True)

    terms_and_conditions = models.BooleanField(default=False)
    safety_rules_and_regulations = models.BooleanField(default=False)


    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} (Booking: {self.booking.booking_code})"
    
    class Meta:
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'
        db_table = 'participants'