import datetime

from collections import deque

from django.core.management.base import BaseCommand
from games.models import Game, Santa, Draw, Exclusion


def get_pair_exclusion(game):
    exclusions = Exclusion.objects.filter(game=game)
    return [(exclusion.giver, exclusion.receiver) for exclusion in exclusions]


def make_draw(game):
    pairs_amount_to_ignore_exclusion = 4
    santas = Santa.objects.filter(games=game)

    partners = deque(santas)
    partners.rotate()
    pairs = list(zip(santas, partners))

    modified_pairs = (
        list(set(pairs) - set(get_pair_exclusion(game)))
            if len(pairs) > pairs_amount_to_ignore_exclusion else list(set(pairs))
    )

    for giver, receiver in modified_pairs:
        draw = Draw.objects.get_or_create(
            game=game,
            giver=giver,
            receiver=receiver
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        games = Game.objects.filter(draw_date=current_date)
        for game in games:
            make_draw(game)
