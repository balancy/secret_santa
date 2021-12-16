import datetime

from collections import deque

from django.core.management.base import BaseCommand
from games.models import Game, Santa, Draw, Exclusion


def get_pair_exclusion(game):
    exclusions = Exclusion.objects.filter(game=game)
    return [(exclusion.giver, exclusion.receiver) for exclusion in exclusions]


def make_rotation(pairs, exclusions):
    pairs_amount_to_ignore_exclusion = 4

    for exclusion in exclusions:
        if (exclusion in pairs) and (len(pairs) > pairs_amount_to_ignore_exclusion):
            pairs = [list(i) for i in pairs]
            exclusion = list(exclusion)

            first_rotation_index = pairs.index(exclusion)
            second_rotation_index = next(i for i, (_, x) in enumerate(pairs)
                if x == exclusion[0])
            third_rotation_index = next(i for i, (_, x) in enumerate(pairs)
                if x == pairs[second_rotation_index][0])

            first_rotation_giver = pairs[first_rotation_index][1]
            second_rotation_giver = pairs[second_rotation_index][1]
            third_rotation_giver = pairs[third_rotation_index][1]

            pairs[first_rotation_index][1] = third_rotation_giver
            pairs[second_rotation_index][1] = first_rotation_giver
            pairs[third_rotation_index][1] = second_rotation_giver

    return pairs


def make_draw(game):
    santas = Santa.objects.filter(games=game)

    partners = deque(santas)
    partners.rotate()
    pairs = list(zip(santas, partners))

    modified_pairs = make_rotation(pairs, get_pair_exclusion(game))

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
