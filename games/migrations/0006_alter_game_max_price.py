# Generated by Django 4.0 on 2021-12-16 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_rename_game_santa_games'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='max_price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='максимальная стоимость подарка'),
        ),
    ]