from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        superuser = User.objects.create(
            email='admin@mail.ru',
            is_superuser=True,
            is_active=True,
            is_staff=True
        )
        superuser.set_password('admin')
        superuser.save()
