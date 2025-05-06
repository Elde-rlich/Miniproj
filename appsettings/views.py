# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.contrib import messages

# @login_required
# def settings_main(request):
#     return render(request, 'appsettings/appsettings.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from .forms import ProfileUpdateForm
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache

@login_required
@never_cache
def settings_main(request):

    profile, created = Profile.objects.get_or_create(user = request.user)
    profile_form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        print("POST request received")
        print("POST request received")
        print("FILES:", request.FILES) 
        # Handle Profile Update
        if 'username' in request.POST and 'email' in request.POST:
            new_username = request.POST.get('username')
            new_email = request.POST.get('email')
            
            # Check if username or email is taken, ignoring the current user
            if User.objects.filter(username=new_username).exists() and new_username != request.user.username:
                messages.error(request, "Username is already taken.")
            elif User.objects.filter(email=new_email).exists() and new_email != request.user.email:
                messages.error(request, "Email is already in use.")
            else:
                try:
                    # Email validation
                    validate_email(new_email)
                    request.user.username = new_username
                    request.user.email = new_email
                    request.user.save()
                    messages.success(request, "Profile updated successfully.")
                except ValidationError:
                    messages.error(request, "Invalid email address.")

        # Handle Password Change
        elif 'current-password' in request.POST and 'new-password' in request.POST and 'confirm-password' in request.POST:
            current_password = request.POST.get('current-password')
            new_password = request.POST.get('new-password')
            confirm_password = request.POST.get('confirm-password')

            # Verify current password
            if not request.user.check_password(current_password):
                messages.error(request, "Current password is incorrect.")
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
            else:
                try:
                    # Password validation
                    validate_password(new_password, request.user)
                    request.user.set_password(new_password)
                    request.user.save()
                    update_session_auth_hash(request, request.user)  # Important to avoid logout
                    messages.success(request, "Password updated successfully.")
                    return redirect('settings_main')
                except ValidationError as e:
                    # Display Django password validation error messages
                    for error in e:
                        messages.error(request, error)
                        
        if 'profile_picture' in request.FILES: 

            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile picture updated successfully.")
                return redirect('settings_main')
            else:
                print("Form errors:", profile_form.errors)
        else:
            print("No file received")

    else:
        profile_form = ProfileUpdateForm(instance=profile)  # Initialize form for GET requests
    
    try:
        profile = request.user.profile
        # Check if profile_picture exists
        if profile.profile_picture:
            profile_picture_url = profile.profile_picture.url
        else:
            profile_picture_url = '/media/profile_pics/default.jpg'  # Fallback to default image
    except ObjectDoesNotExist:
        profile_picture_url = '/media/profile_pics/default.jpg'  # Fallback if the profile doesn't exist

    # Ensure the form is always passed to the template
    return render(request, 'appsettings/appsettings.html', {'user': request.user, 'profile_form': profile_form, 'profile_picture_url': profile_picture_url})
