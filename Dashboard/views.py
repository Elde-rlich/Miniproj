from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@login_required
@never_cache
def home(request):
    user_profile = request.user.profile
    # Check if the user has a profile picture
    if not user_profile.profile_picture:
        user_profile.profile_picture = 'profile_pics/default.jpg'  # Set default image if none exists
        user_profile.save()

    return render(request, 'dashboard/dashboard.html', {'user_profile': user_profile})