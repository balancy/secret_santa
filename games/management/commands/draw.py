import datetime
import os

from collections import deque
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from email.message import EmailMessage

from games.models import Game, Santa, Draw, Exclusion


def send_email(subject, to_addr, from_addr, body_text):
    send_mail(
        subject,
        body_text,
        from_addr,
        [to_addr],
        fail_silently=False,
    )


def make_and_send_email_message(game, from_adress):
    draws = Draw.objects.filter(game=game)

    for draw in draws:
        subject = f'Жеребьевка в игре {game.name} проведена!'
        body_text = (
            f'Жеребьевка в игре {game.name} проведена!\r\n' +
            'Спешу сообщить кто тебе выпал.\r\n' +
            f'Ваш игрок: {draw.receiver.user.username}\r\n' +
            f'Адрес эл. почты: {draw.receiver.user.email}\r\n' +
            f'Письмо Санте: {draw.receiver.letter_to_santa}\r\n' +
            f'Вишлист: {draw.receiver.wishlist}\r\n'
        )

        send_email(
            subject,
            draw.giver.user.email,
            from_adress,
            body_text
        )


def get_pair_exclusion(game):
    exclusions = Exclusion.objects.filter(game=game)
    return [(exclusion.giver, exclusion.receiver) for exclusion in exclusions]


def make_rotation(pairs, exclusions):
    pairs_amount_to_ignore_exclusion = 3

    for exclusion in exclusions:
        if (exclusion in pairs) and (len(pairs) > pairs_amount_to_ignore_exclusion):
            pairs = [list(i) for i in pairs]
            exclusion = list(exclusion)

            first_rotation_index = pairs.index(exclusion)
            second_rotation_index = next(
                i for i, (_, required_element) in enumerate(pairs)
                if required_element == exclusion[0]
            )
            third_rotation_index = next(
                i for i, (_, required_element) in enumerate(pairs)
                if required_element == pairs[second_rotation_index][0]
            )

            first_rotation_giver = pairs[first_rotation_index][1]
            second_rotation_giver = pairs[second_rotation_index][1]
            third_rotation_giver = pairs[third_rotation_index][1]

            pairs[first_rotation_index][1] = third_rotation_giver
            pairs[second_rotation_index][1] = first_rotation_giver
            pairs[third_rotation_index][1] = second_rotation_giver

    return pairs


def is_exclusions_in_pairs(pairs, exclusions):
    for exclusion in exclusions:
        if (exclusion in pairs):
            return True
    return False


def make_draw(game):
    santas = Santa.objects.filter(games=game)

    partners = deque(santas)
    partners.rotate()
    pairs = list(zip(santas, partners))

    exclusions = get_pair_exclusion(game)

    modified_pairs = make_rotation(pairs, exclusions)

    while True:
        if is_exclusions_in_pairs(modified_pairs, exclusions):
            modified_pairs = make_rotation(pairs, exclusions)
        else:
            break

    for giver, receiver in modified_pairs:
        draw = Draw.objects.get_or_create(
            game=game,
            giver=giver,
            receiver=receiver
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        from_adress = os.getenv('from_adress')

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        games = Game.objects.filter(draw_date=current_date)
        for game in games:
            make_draw(game)
            make_and_send_email_message(game, from_adress)
