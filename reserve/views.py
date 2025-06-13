from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import MemberRegistrationForm, BookingForm, HotelForm, HotelTableForm, ActivityForm, EventForm, TeeTimeForm, MemberProfileUpdateForm
from .models import Booking, Hotel, HotelTable, Activity, Event, TeeTime, MemberProfile
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone

# --- Client Interface Views ---


@login_required
def member_dashboard(request):
    """
    View for the member's dashboard, showing their bookings.
    """
    try:
        member_profile = request.user.profile
    except MemberProfile.DoesNotExist:
        messages.error(request, "You do not have a profile. Please contact support.")
        return redirect('update_member_profile')  # Redirect to login or another appropriate page
    if member_profile.membership_status != 'approved':
        messages.warning(request, "Please await approval to edit your profile and access the dashboard.")
        return render(request, 'awaiting_approval.html')  # Create a new template for this message
    bookings = Booking.objects.filter(member=member_profile).order_by('scheduled_date')
    return render(request, 'member_dashboard.html', {'bookings': bookings})


@login_required
def create_booking(request):
    """
    View for creating a new booking.
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.member = request.user.profile  # Associate with the logged-in member
            booking.save()
            messages.success(request, 'Booking created successfully!')
            return redirect('member_dashboard')
        else:
            messages.error(request, 'Booking creation failed. Please correct the errors below.')
    else:
        form = BookingForm()
    return render(request, 'create_booking.html', {'form': form})





# --- Staff Interface Views ---

def is_staff(user):
    return user.is_staff  # Or any other criteria for staff

@login_required
@user_passes_test(is_staff)
def staff_dashboard(request):
    """
    View for the staff dashboard, showing all bookings and management options.
    """
    bookings = Booking.objects.all().order_by('scheduled_date')
    return render(request, 'staff/staff_dashboard.html', {'bookings': bookings})

# Hotel Management
@login_required
@user_passes_test(is_staff)
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'staff/hotel/hotel_list.html', {'hotels': hotels})

@login_required
@user_passes_test(is_staff)
def hotel_create(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hotel created successfully.")
            return redirect('hotel_list')
    else:
        form = HotelForm()
    return render(request, 'staff/hotel/hotel_form.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def hotel_update(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        form = HotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, "Hotel updated successfully.")
            return redirect('hotel_list')
    else:
        form = HotelForm(instance=hotel)
    return render(request, 'staff/hotel/hotel_form.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def hotel_delete(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        hotel.delete()
        messages.success(request, "Hotel deleted successfully.")
        return redirect('hotel_list')
    return render(request, 'staff/hotel/hotel_confirm_delete.html', {'hotel': hotel})

# Booking Management
@login_required
@user_passes_test(is_staff)
def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'staff/booking/booking_list.html', {'bookings': bookings})

@login_required
@user_passes_test(is_staff)
def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully.")
            return redirect('booking_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'staff/booking/booking_form.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Booking deleted successfully.")
        return redirect('booking_list')
    return render(request, 'staff/booking/booking_confirm_delete.html', {'booking': booking})

# Member Management
@login_required
@user_passes_test(is_staff)
def member_list(request):
    members = MemberProfile.objects.all()
    return render(request, 'staff/member/member_list.html', {'members': members})

@login_required
@user_passes_test(is_staff)
def member_detail(request, pk):
    member = get_object_or_404(MemberProfile, pk=pk)
    return render(request, 'staff/member/member_detail.html', {'member': member})

@login_required
@user_passes_test(is_staff)
def member_update(request, pk):
    member = get_object_or_404(MemberProfile, pk=pk)
    if request.method == 'POST':
        form = MemberProfileUpdateForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Member profile updated successfully.")
            return redirect('member_detail', pk=member.pk)
    else:
        form = MemberProfileUpdateForm(instance=member)
    return render(request, 'staff/member/member_form.html', {'form': form})

# Activity Management
@login_required
@user_passes_test(is_staff)
def activity_list(request):
    activities = Activity.objects.all()
    return render(request, 'staff/activity/activity_list.html', {'activities': activities})

@login_required
@user_passes_test(is_staff)
def activity_create(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Activity created successfully.")
            return redirect('activity_list')
    else:
        form = ActivityForm()
    return render(request, 'staff/activity/activity_form.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def activity_update(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, "Activity updated successfully.")
            return redirect('activity_list')
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'staff/activity/activity_form.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        activity.delete()
        messages.success(request, "Activity deleted successfully.")
        return redirect('activity_list')
    return render(request, 'staff/activity/activity_confirm_delete.html', {'activity': activity})

# Event Management
@login_required
@user_passes_test(is_staff)
def event_list(request):
    events = Event.objects.all()
    return render(request, 'staff/event/event_list.html', {'events': events})

@login_required
@user_passes_test(is_staff)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully.")
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'staff/event/event_form.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'staff/event/event_form.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect('event_list')
    return render(request, 'staff/event/event_confirm_delete.html', {'event': event})


@login_required
@user_passes_test(is_staff)
def tee_time_list(request):
    """
    View to list all TeeTime instances in the system.
    """
    tee_times = TeeTime.objects.all().order_by('start_time')  # Adjust field name to your model's datetime
    return render(request, 'staff/tee_time/tee_time_list.html', {'tee_times': tee_times})

@login_required
@user_passes_test(is_staff)
def tee_time_detail(request, pk):
    """
    View to show details of a single TeeTime.
    """
    tee_time = get_object_or_404(TeeTime, pk=pk)
    return render(request, 'staff/tee_time/tee_time_detail.html', {'tee_time': tee_time})

@login_required
@user_passes_test(is_staff)
def tee_time_create(request):
    """
    View to create a new TeeTime.
    """
    if request.method == 'POST':
        form = TeeTimeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tee time created successfully.')
            return redirect('tee_time_list')
    else:
        form = TeeTimeForm()
    return render(request, 'staff/tee_time/tee_time_form.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def tee_time_update(request, pk):
    """
    View to edit an existing TeeTime.
    """
    tee_time = get_object_or_404(TeeTime, pk=pk)
    if request.method == 'POST':
        form = TeeTimeForm(request.POST, instance=tee_time)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tee time updated successfully.')
            return redirect('tee_time_list')
    else:
        form = TeeTimeForm(instance=tee_time)
    return render(request, 'staff/tee_time/tee_time_form.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def tee_time_delete(request, pk):
    """
    View to delete a TeeTime.
    """
    tee_time = get_object_or_404(TeeTime, pk=pk)
    if request.method == 'POST':
        tee_time.delete()
        messages.success(request, 'Tee time deleted successfully.')
        return redirect('tee_time_list')
    return render(request, 'staff/tee_time/tee_time_confirm_delete.html', {'tee_time': tee_time})
