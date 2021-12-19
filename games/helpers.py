import hashlib
import hmac

import requests

from .models import Santa
from secret_santa.settings import BITLY_TOKEN, HASH_KEY


def create_santa_for_user(user, wishlist='', letter=''):
    Santa.objects.create(user=user, wishlist=wishlist, letter_to_santa=letter)


def create_bitlink(link):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {'Authorization': f'Bearer {BITLY_TOKEN}'}
    payload = {'long_url': link, 'domain': 'bit.ly'}
    res = requests.post(url, json=payload, headers=headers)
    res.raise_for_status()

    return res.json()['id']


def hash_value(value):
    value = str(value)

    h = '{}_{}'.format(
        hmac.new(
            HASH_KEY.encode(), value.encode(), hashlib.sha256
        ).hexdigest(),
        value,
    )

    return h


def is_hash_correct(hashed_value):
    if hashed_value is None:
        return None

    if '_' not in hashed_value:
        return None

    _, id = hashed_value.split('_')

    return hashed_value == hash_value(id)
