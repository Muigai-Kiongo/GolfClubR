from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Client Interface
    path('', views.member_dashboard, name='member_dashboard'),
    path('booking/create/', views.create_booking, name='create_booking'),
    path('payment/',views.payment,name='payment'),

    # Staff Interface
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/reports',views.reports_view, name='staff_reports'),

    path('staff/hotels/', views.hotel_list, name='hotel_list'),
    path('staff/hotels/create/', views.hotel_create, name='hotel_create'),
    path('staff/hotels/update/<int:pk>/', views.hotel_update, name='hotel_update'),
    path('staff/hotels/delete/<int:pk>/', views.hotel_delete, name='hotel_delete'),

    path('staff/bookings/', views.booking_list, name='booking_list'),
    path('staff/bookings/update/<int:pk>/', views.booking_update, name='booking_update'),
    path('staff/bookings/delete/<int:pk>/', views.booking_delete, name='booking_delete'),

    path('staff/members/', views.member_list, name='member_list'),
    path('staff/members/<int:pk>/', views.member_detail, name='member_detail'),
    path('staff/members/update/<int:pk>/', views.member_update, name='member_update'),

    path('staff/activities/', views.activity_list, name='activity_list'),
    path('staff/activities/create/', views.activity_create, name='activity_create'),
    path('staff/activities/update/<int:pk>/', views.activity_update, name='activity_update'),
    path('staff/activities/delete/<int:pk>/', views.activity_delete, name='activity_delete'),

    path('staff/events/', views.event_list, name='event_list'),
    path('staff/events/create/', views.event_create, name='event_create'),
    path('staff/events/update/<int:pk>/', views.event_update, name='event_update'),
    path('staff/events/delete/<int:pk>/', views.event_delete, name='event_delete'),

    path('staff/tee_times/', views.tee_time_list, name='tee_time_list'),
    path('staff/tee_times/create/', views.tee_time_create, name='tee_time_create'),
    path('staff/tee_times/<int:pk>/', views.tee_time_detail, name='tee_time_detail'),
    path('staff/tee_times/<int:pk>/edit/', views.tee_time_update, name='tee_time_update'),
    path('staff/tee_times/<int:pk>/delete/', views.tee_time_delete, name='tee_time_delete'),


]
