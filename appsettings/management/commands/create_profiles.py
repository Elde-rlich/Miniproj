from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from appsettings.models import Profile

class Command(BaseCommand):
    help = 'Create profile instances for all users'

    def handle(self, *args, **kwargs):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        for user in users_without_profiles:
            Profile.objects.create(user=user)
            self.stdout.write(f'Profile created for user: {user.username}')
        self.stdout.write('All profiles created successfully.')
