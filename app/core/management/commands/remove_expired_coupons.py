from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Removes expired coupons for all users'

    def handle(self, *args, **options):
        user = get_user_model()
        users = user.objects.all()

        for user in users:
            user.remove_expired_coupons()
            self.stdout.write(self.style.SUCCESS(
                f"Removed expired coupons for user '{user.email}'"))
