from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Reset admin password'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        try:
            admin = User.objects.get(username='admin')
            admin.set_password('newpassword123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Password reset successful!'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Admin user not found'))
