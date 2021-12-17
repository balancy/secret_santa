from .models import Santa
import requests
from secret_santa.settings import BITLY_TOKEN


def create_santa_for_user(user, wishlist, letter):
    Santa.objects.create(user=user, wishlist=wishlist, letter_to_santa=letter)


def create_bitlink(link):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {'Authorization': f'Bearer {BITLY_TOKEN}'}
    payload = {'long_url': link, 'domain': 'bit.ly'}
    res = requests.post(url, json=payload, headers=headers)
    res.raise_for_status()

    return res.json()['id']
