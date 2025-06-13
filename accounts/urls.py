from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('register/',views.signUp, name='register'),
    path('profile/update/', views.update_member_profile, name='update_member_profile'),

]