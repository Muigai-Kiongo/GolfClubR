from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class MemberProfile(models.Model):
    MEMBERSHIP_STATUS = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    )

    MEMBERSHIP_TYPE = (
        ('full', 'Full'),
        ('social', 'Social'),
        ('junior', 'Junior'),
        ('senior', 'Senior'),
        ('corporate', 'Corporate'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    membership_status = models.CharField(
        max_length=10,
        choices=MEMBERSHIP_STATUS,
        default='pending',
        help_text="Membership approval status"
    )
    membership_type = models.CharField(
        max_length=10,
        choices=MEMBERSHIP_TYPE,
        default='full',
        verbose_name='Membership Type'
    )
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='Phone Number')
    address = models.TextField(blank=True, verbose_name='Address')
    joined_date = models.DateTimeField(default=timezone.now, verbose_name='Joined Date')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Date of Birth')
    handicap = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, verbose_name='Golf Handicap')
    emergency_contact_name = models.CharField(max_length=200, blank=True, verbose_name='Emergency Contact Name')
    emergency_contact_phone = models.CharField(max_length=20, blank=True, verbose_name='Emergency Contact Phone')

    class Meta:
        verbose_name = 'Member Profile'
        verbose_name_plural = 'Member Profiles'

    def __str__(self):
        return f'{self.user.username} Profile - Status: {self.get_membership_status_display()}'


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=20, blank=True)
    amenities = models.TextField(blank=True, help_text="List of amenities offered by the hotel (e.g., swimming pool, gym, spa)")
    rooms_available = models.PositiveIntegerField(default=0, verbose_name="Number of Rooms Available")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Price Per Night")

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'

    def __str__(self):
        return self.name


class HotelTable(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='tables')
    table_number = models.IntegerField(verbose_name='Table Number')
    capacity = models.IntegerField(verbose_name='Table Capacity')

    class Meta:
        verbose_name = 'Hotel Table'
        verbose_name_plural = 'Hotel Tables'
        unique_together = ('hotel', 'table_number')  # Ensure table numbers are unique within a hotel

    def __str__(self):
        return f'Table {self.table_number} at {self.hotel.name}'


class GolfCourse(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=300, blank=True)
    holes = models.IntegerField(default=18)
    par = models.IntegerField(default=72)

    class Meta:
        verbose_name = 'Golf Course'
        verbose_name_plural = 'Golf Courses'

    def __str__(self):
        return self.name


class TeeTime(models.Model):
    golf_course = models.ForeignKey(GolfCourse, on_delete=models.CASCADE, related_name='tee_times')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_players = models.IntegerField(default=4)
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Price per Player")

    class Meta:
        verbose_name = 'Tee Time'
        verbose_name_plural = 'Tee Times'
        ordering = ['start_time']

    def __str__(self):
        return f'{self.golf_course.name} - {self.start_time.strftime("%Y-%m-%d %H:%M")}'


class Activity(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum number of participants.")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Price per Participant")

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
        ordering = ['start_time']

    def __str__(self):
        return f'{self.name} ({self.start_time.strftime("%Y-%m-%d %H:%M")})'


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200, blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum number of attendees.")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Price per Attendee")

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['event_date', 'start_time']

    def __str__(self):
        return f'{self.name} on {self.event_date}'


class Booking(models.Model):
    BOOKING_TYPE_CHOICES = (
        ('hotel', 'Hotel Room'),
        ('table', 'Hotel Table'),
        ('activity', 'Activity'),
        ('event', 'Event'),
        ('tee_time', 'Tee Time'),
    )
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='bookings')
    booking_type = models.CharField(max_length=10, choices=BOOKING_TYPE_CHOICES)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, blank=True, null=True)
    hotel_table = models.ForeignKey(HotelTable, on_delete=models.CASCADE, blank=True, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    tee_time = models.ForeignKey(TeeTime, on_delete=models.CASCADE, blank=True, null=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateTimeField(verbose_name='Scheduled Date and Time')
    number_of_guests = models.PositiveIntegerField(default=1, verbose_name='Number of Guests')
    notes = models.TextField(blank=True, verbose_name='Special Requests/Notes')

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-booking_date']

    def clean(self):
        from django.core.exceptions import ValidationError

        # Ensure booking_type matches the related foreign key
        if self.booking_type == 'hotel' and not self.hotel:
            raise ValidationError('Hotel must be set for hotel bookings.')
        if self.booking_type == 'table' and not self.hotel_table:
            raise ValidationError('Hotel Table must be set for hotel table bookings.')
        if self.booking_type == 'activity' and not self.activity:
            raise ValidationError('Activity must be set for activity bookings.')
        if self.booking_type == 'event' and not self.event:
            raise ValidationError('Event must be set for event bookings.')
        if self.booking_type == 'tee_time' and not self.tee_time:
            raise ValidationError('Tee Time must be set for tee time bookings.')

        # Ensure only one foreign key set depending on booking_type
        related = {
            'hotel': self.hotel,
            'table': self.hotel_table,
            'activity': self.activity,
            'event': self.event,
            'tee_time': self.tee_time,
        }
        for key, val in related.items():
            if key != self.booking_type and val is not None:
                raise ValidationError(f'{key.title()} must be null if booking type is {self.booking_type}.')

    def __str__(self):
        return f'{self.booking_type.title()} booking for {self.member.user.username} at {self.scheduled_date}'
