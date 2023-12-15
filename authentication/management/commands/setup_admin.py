import os

from authentication.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create an admin superuser - does not throw Exception if user exists'

    def handle(self, *args, **options):
        user = User.objects.filter(username=os.getenv('DJANGO_SUPERUSER_USERNAME','admin'))
        
        if(not user.exists()):
            User.objects.create_superuser(
                    first_name=os.getenv('DJANGO_SUPERUSER_FIRSTNAME','super'),
                    last_name=os.getenv('DJANGO_SUPERUSER_LASTNAME','admin'),
                    username=os.getenv('DJANGO_SUPERUSER_USERNAME','admin'),
                    email=os.getenv('DJANGO_SUPERUSER_EMAIL','admin@viza.com'),
                    password=os.getenv('DJANGO_SUPERUSER_PASSWORD','admin.321')
                    )