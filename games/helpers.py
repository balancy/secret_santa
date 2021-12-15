from .models import Santa


def create_santa_for_user(user):
    Santa.objects.create(user=user)
