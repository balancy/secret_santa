from itertools import combinations

from django.core.management.base import BaseCommand, CommandError
from games.models import Game, Santa, Draw, Exclusion


def get_pair_exclusion(game):
    return Exclusion.objects.filter(game=game)


def make_draw(game):
    santas = Santa.objects.filter(game=game)

    pairs = list(combinations(santas, 2))
    for giver, receiver in pairs:
         draw = Draw.objects.get_or_create(
             game=game,
             giver=giver,
             receiver=receiver
         )


class Command(BaseCommand):
    def handle(self, *args, **options):
        game = Game.objects.first()
        make_draw(game)
