import random

from more_itertools import chunked

from django.core.management.base import BaseCommand, CommandError
from games.models import Game, Santa, Draw, Exclusion


def make_draw(game):
    santas = Santa.objects.filter(game=game)

    random.shuffle(santas)
    pairs = list(chunked(santas, 2))
    if len(santas) % 2 != 0:
        pairs[-1].append(santas[0])

    for giver, receiver in pairs:
        draw = Draw.objects.create(
            game=game,
            giver=giver,
            receiver=receiver
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        game = Game.objects.all().first()
        make_draw(game)
