import datetime
import os
import smtplib

from collections import deque
from django.core.management.base import BaseCommand
from email.message import EmailMessage

from games.models import Game, Santa, Draw, Exclusion


def send_email(smtp_server, subject, to_addr, from_addr, body_text):
    email_body = (
        f'From: {from_addr}\r\n' +
        'To: {to_addr}\r\n' +
        'Subject: {subject}\r\n{body_text}'
    )
    msg = EmailMessage()
    msg.set_content(body_text)
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr

    smtp_server.send_message(msg)


def make_and_send_email_message(game, smtp_server, from_adress):
    draws = Draw.objects.filter(game=game)

    for draw in draws:
        subject = f'Жеребьевка в игре {game.name} проведена!'
        body_text = (
            f'Жеребьевка в игре {game.name} проведена!\r\n' +
            'Спешу сообщить кто тебе выпал.\r\n' +
            'Ваш игрок: {draw.receiver.user.username}\r\n' +
            'Адрес эл. почты: {draw.receiver.user.email}\r\n' +
            'Письмо Санте: {draw.receiver.letter_to_santa}\r\n' +
            'Вишлист: {draw.receiver.wishlist}'
        )

        send_email(
            smtp_server,
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
        from_adress = os.getenv('from_adress')
        smtp_server = smtplib.SMTP_SSL(
            os.getenv('smtp_host'),
            port=os.getenv('smtp_port')
        )
        smtp_server.login(
            os.getenv('mail_server_login'),
            os.getenv('mail_server_password')
        )

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        games = Game.objects.filter(draw_date=current_date)
        for game in games:
            make_draw(game)
            make_and_send_email_message(game, smtp_server, from_adress)

        smtp_server.quit()
