from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MemberProfile, Booking, Hotel, HotelTable, Activity, Event, TeeTime
from django.contrib.auth.models import User

class MemberRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20, required=False, help_text="Optional")
    address = forms.CharField(widget=forms.Textarea, required=False, help_text="Optional")
    membership_type = forms.ChoiceField(choices=MemberProfile.MEMBERSHIP_TYPE, required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, help_text="Optional")
    handicap = forms.DecimalField(required=False, help_text="Optional", max_digits=5, decimal_places=1)
    emergency_contact_name = forms.CharField(max_length=200, required=False, help_text="Optional")
    emergency_contact_phone = forms.CharField(max_length=20, required=False, help_text="Optional")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = MemberProfile(
                user=user,
                phone_number=self.cleaned_data.get('phone_number', ''),
                address=self.cleaned_data.get('address', ''),
                membership_type=self.cleaned_data.get('membership_type', 'full'),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                handicap=self.cleaned_data.get('handicap'),
                emergency_contact_name=self.cleaned_data.get('emergency_contact_name', ''),
                emergency_contact_phone=self.cleaned_data.get('emergency_contact_phone', ''),
            )
            profile.save()
        return user


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'booking_type',
            'hotel',
            'hotel_table',
            'activity',
            'event',
            'tee_time',
            'scheduled_date',
            'number_of_guests',
            'notes'
        ]
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'number_of_guests': forms.NumberInput(attrs={'min': 1}),  # Ensure at least 1 guest
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set optional fields to not required and hidden by default
        for field in ['hotel', 'hotel_table', 'activity', 'event', 'tee_time']:
            self.fields[field].required = False
            self.fields[field].widget.attrs['style'] = 'display:none;'

        booking_type = self.data.get('booking_type') or self.initial.get('booking_type')
        if booking_type == 'hotel':
            self.fields['hotel'].required = True
            self.fields['hotel'].widget.attrs['style'] = 'display:block;'
        elif booking_type == 'table':
            self.fields['hotel_table'].required = True
            self.fields['hotel_table'].widget.attrs['style'] = 'display:block;'
        elif booking_type == 'activity':
            self.fields['activity'].required = True
            self.fields['activity'].widget.attrs['style'] = 'display:block;'
        elif booking_type == 'event':
            self.fields['event'].required = True
            self.fields['event'].widget.attrs['style'] = 'display:block;'
        elif booking_type == 'tee_time':
            self.fields['tee_time'].required = True
            self.fields['tee_time'].widget.attrs['style'] = 'display:block;'

    def clean(self):
        cleaned_data = super().clean()
        booking_type = cleaned_data.get('booking_type')
        field_map = {
            'hotel': 'hotel',
            'table': 'hotel_table',
            'activity': 'activity',
            'event': 'event',
            'tee_time': 'tee_time',
        }
        for key, field in field_map.items():
            val = cleaned_data.get(field)
            if booking_type == key and not val:
                self.add_error(field, f"This field is required for {booking_type} bookings.")
            if booking_type != key and val not in [None, '', []]:
                self.add_error(field, f"This field must be empty for booking type {booking_type}.")


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'amenities': forms.Textarea(attrs={'rows': 3}),
            'price_per_night': forms.NumberInput(attrs={'min': 0}),
        }


class HotelTableForm(forms.ModelForm):
    class Meta:
        model = HotelTable
        fields = '__all__'


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'capacity': forms.NumberInput(attrs={'min': 1}),
            'price': forms.NumberInput(attrs={'min': 0}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'capacity': forms.NumberInput(attrs={'min': 1}),
            'price': forms.NumberInput(attrs={'min': 0}),
        }


class TeeTimeForm(forms.ModelForm):
    class Meta:
        model = TeeTime
        fields = '__all__'
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'max_players': forms.NumberInput(attrs={'min': 1}),
            'price': forms.NumberInput(attrs={'min': 0}),
        }


class MemberProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['phone_number', 'address', 'membership_type', 'date_of_birth', 'handicap', 'emergency_contact_name', 'emergency_contact_phone']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'handicap': forms.NumberInput(attrs={'min': 0}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
