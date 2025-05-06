from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache

@never_cache
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            messages.error(request, 'There was an error in your registration. Please check the form and try again.')
            print(form.errors) 
    else:
        form = UserRegisterForm()
    return render(request, 'authapp/register.html', {'form': form})


@login_required
@never_cache
def home(request):
    user_profile = request.user.profile
    # Check if the user has a profile picture
    if not user_profile.profile_picture:
        user_profile.profile_picture = 'profile_pics/default.jpg'  # Set default image if none exists
        user_profile.save()

    return render(request, 'dashboard/dashboard.html', {'user_profile': user_profile})



class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return

        email = sociallogin.account.extra_data.get('email')
        try:
            user = User.objects.get(email=email)
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass
