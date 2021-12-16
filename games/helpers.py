from .models import Santa


def create_santa_for_user(user, wishlist, letter):
    Santa.objects.create(user=user, wishlist=wishlist, letter_to_santa=letter)
