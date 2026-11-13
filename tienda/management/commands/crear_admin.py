
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Crea o actualiza el administrador desde variables de entorno'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        if not username or not email or not password:
            raise CommandError(
                'Faltan las variables ADMIN_USERNAME, ADMIN_EMAIL o ADMIN_PASSWORD'
            )

        User = get_user_model()

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email}
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS('Administrador creado o actualizado correctamente.')
        )
