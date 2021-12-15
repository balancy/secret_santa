from collections import deque

from django.core.management.base import BaseCommand
from games.models import Game, Santa, Draw, Exclusion


def get_pair_exclusion(game):
    exclusions = Exclusion.objects.filter(game=game)
    return [(exclusion.giver, exclusion.receiver) for exclusion in exclusions]


def make_draw(game):
    santas = Santa.objects.filter(game=game)

    partners = deque(santas)
    partners.rotate()
    pairs = list(zip(santas, partners))

    filtered_pairs = list(set(pairs) - set(get_pair_exclusion(game)))

    for giver, receiver in filtered_pairs:
        draw = Draw.objects.get_or_create(
            game=game,
            giver=giver,
            receiver=receiver
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        game = Game.objects.first()
        make_draw(game)
