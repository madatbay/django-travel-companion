import secrets
import string

from django.core.management.base import BaseCommand
from user.models import User


def generate_password(length: int):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for i in range(length))


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            email = "root@admin.com"
            password = generate_password(15)
            admin = User.objects.create_superuser(email=email, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
            print(
                f"_________________________________________________ \n"
                f"Initial ADMIN ACCOUNT email={email}, password={password} \n"
                f"DO CHANGE THE PASSWORD AFTER FIRST LOGIN \n"
                f"_________________________________________________ \n"
            )
