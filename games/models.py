from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass


class Game(models.Model):
    name = models.CharField(
        'название',
        max_length=30,
        db_index=True,
    )

    coordinator = models.ForeignKey(
        CustomUser,
        related_name='games_coordinators',
        verbose_name='организатор',
        on_delete=models.PROTECT,
    )

    max_price = models.PositiveIntegerField('максимальная стоимость подарка')
    draw_date = models.DateTimeField('Дата жеребьёвки')
    gift_date = models.DateTimeField('Дата отправки подарка')

    class Meta:
        verbose_name = 'игра'
        verbose_name_plural = 'игры'

    def __str__(self):
        return f'Игра {self.name}'


class Santa(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.PROTECT,
    )

    game = models.ManyToManyField(
        Game,
        related_name='santas',
        verbose_name='игра',
    )

    wishlist = models.TextField('Желания', null=True)
    letter_to_santa = models.TextField('Письмо Санте', null=True)

    class Meta:
        verbose_name = 'санта'
        verbose_name_plural = 'санты'

    def __str__(self):
        return f'Санта {self.user.last_name}'


class Draw(models.Model):
    game = models.ForeignKey(
        Game,
        related_name='draws',
        verbose_name='игра',
        on_delete=models.PROTECT,
    )

    giver = models.ForeignKey(
        Santa,
        related_name='draws_givers',
        verbose_name='даритель',
        on_delete=models.PROTECT,
    )

    receiver = models.ForeignKey(
        Santa,
        related_name='draws_receivers',
        verbose_name='одаряемый',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'жеребьёвка'
        verbose_name_plural = 'жеребьёвки'
