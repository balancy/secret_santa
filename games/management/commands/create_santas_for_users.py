from django.core.management.base import BaseCommand

from games.models import CustomUser, Santa


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = CustomUser.objects.all()
        for user in users:
            santa_for_user = Santa.objects.filter(user=user)
            if not santa_for_user:
                Santa.objects.create(user=user)
