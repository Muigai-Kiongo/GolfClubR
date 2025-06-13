from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from reserve.forms import MemberProfileUpdateForm

def signUp (request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            redirect('login')
            messages.success(request, ('Registration successful!'))
            return redirect('home')
    else:

        form = UserCreationForm()

        context= {
            'form':form,
            'title': 'Register'
        }

    return render(request, 'registration/register.html', context)


@login_required
def update_member_profile(request):
    """
    View for updating a member's profile information.
    """
    member_profile = request.user.profile
    if request.method == 'POST':
        form = MemberProfileUpdateForm(request.POST, instance=member_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('member_dashboard')
        else:
            messages.error(request, 'Profile update failed. Please correct the errors below.')
    else:
        form = MemberProfileUpdateForm(instance=member_profile)
    return render(request, 'profile/update_member_profile.html', {'form': form})